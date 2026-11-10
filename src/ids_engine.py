"""
AI Engine for Aegis-Sentinel.
Trains a Random Forest model to detect network intrusions.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

class IDSEngine:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.protocol_encoder = LabelEncoder()
        self.is_trained = False

    def load_and_prepare_data(self, filepath):
        """Carga el CSV y prepara los datos para el modelo."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset not found at {filepath}")
            
        df = pd.read_csv(filepath)
        
        # 1. Codificar variables categóricas (protocol_type: TCP, UDP, ICMP -> 0, 1, 2)
        self.protocol_encoder.fit(df['protocol_type'])
        df['protocol_type_encoded'] = self.protocol_encoder.transform(df['protocol_type'])
        
        # 2. Separar características (X) y el objetivo (y)
        features = ['duration', 'src_bytes', 'dst_bytes', 'failed_logins', 'protocol_type_encoded', 'count']
        X = df[features]
        y = df['class']
        
        return X, y

    def train(self, filepath):
        """Entrena el modelo de Machine Learning."""
        X, y = self.load_and_prepare_data(filepath)
        
        # Dividir en datos de entrenamiento (80%) y prueba (20%)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Entrenar el modelo
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluar el modelo
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        return accuracy, classification_report(y_test, y_pred)

    def predict(self, duration, src_bytes, dst_bytes, failed_logins, protocol_type, count):
        """Predice si una nueva conexión es un ataque o tráfico normal."""
        if not self.is_trained:
            raise RuntimeError("Model must be trained before predicting.")
            
        # Codificar el protocolo (con Guardrail por si llega uno desconocido)
        try:
            protocol_encoded = self.protocol_encoder.transform([protocol_type])[0]
        except ValueError:
            protocol_encoded = 0 # Default a TCP si es desconocido
            
        # Crear el DataFrame de entrada (mismas columnas que el entrenamiento)
        input_data = pd.DataFrame([{
            'duration': duration,
            'src_bytes': src_bytes,
            'dst_bytes': dst_bytes,
            'failed_logins': failed_logins,
            'protocol_type_encoded': protocol_encoded,
            'count': count
        }])
        
        # Predecir (0 = Normal, 1 = Ataque)
        prediction = self.model.predict(input_data)[0]
        probability = self.model.predict_proba(input_data)[0][1] # Probabilidad de ataque
        
        return prediction, probability

# --- Bloque de prueba ---
if __name__ == "__main__":
    print("🛡️ Inicializando Aegis-Sentinel AI Engine...")
    
    # Ruta al dataset (un nivel arriba de src/)
    dataset_path = os.path.join(os.path.dirname(__file__), "../network_traffic.csv")
    
    engine = IDSEngine()
    
    print("⏳ Entrenando el modelo con Random Forest...")
    accuracy, report = engine.train(dataset_path)
    
    print(f"\n✅ Modelo entrenado. Precisión (Accuracy): {accuracy * 100:.2f}%\n")
    print("📊 Reporte de Clasificación:")
    print(report)
    
    # Prueba rápida: Simulando un ataque de fuerza bruta (muchos logins fallidos, muchas conexiones)
    print("\n🔍 Analizando conexión sospechosa...")
    pred, prob = engine.predict(
        duration=0.5, 
        src_bytes=100, 
        dst_bytes=50, 
        failed_logins=15, # ¡Muchos fallos!
        protocol_type="TCP", 
        count=120         # ¡Muchas conexiones!
    )
    
    if pred == 1:
        print(f"🚨 ¡ALERTA! Ataque detectado. Probabilidad: {prob * 100:.2f}%")
    else:
        print(f"✅ Tráfico normal. Probabilidad de ataque: {prob * 100:.2f}%")
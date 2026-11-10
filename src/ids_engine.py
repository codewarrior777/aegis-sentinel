"""
AI Engine for Aegis-Sentinel.
Trains a Random Forest model and saves it to disk (MLOps).
"""

import os
import joblib
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
        # Ruta donde se guardará el modelo entrenado
        self.model_path = os.path.join(os.path.dirname(__file__), "../ids_model.joblib")

    def load_and_prepare_data(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset not found at {filepath}")
            
        df = pd.read_csv(filepath)
        
        self.protocol_encoder.fit(df['protocol_type'])
        df['protocol_type_encoded'] = self.protocol_encoder.transform(df['protocol_type'])
        
        features = ['duration', 'src_bytes', 'dst_bytes', 'failed_logins', 'protocol_type_encoded', 'count']
        X = df[features]
        y = df['class']
        
        return X, y

    def train(self, filepath):
        """Entrena el modelo o lo carga si ya existe en disco."""
        
        # 1. MLOps: Si el modelo ya está guardado, lo cargamos (Ahorra tiempo y recursos)
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            print("✅ Modelo cargado desde el disco.")
            return 1.0, "Model loaded from disk."

        # 2. Si no existe, lo entrenamos desde cero
        X, y = self.load_and_prepare_data(filepath)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # 3. Guardamos el modelo entrenado para el futuro
        joblib.dump(self.model, self.model_path)
        print("✅ Modelo entrenado y guardado en disco.")
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy, classification_report(y_test, y_pred)

    def predict(self, duration, src_bytes, dst_bytes, failed_logins, protocol_type, count):
        if not self.is_trained:
            raise RuntimeError("Model must be trained before predicting.")
            
        try:
            protocol_encoded = self.protocol_encoder.transform([protocol_type])[0]
        except ValueError:
            protocol_encoded = 0 
            
        input_data = pd.DataFrame([{
            'duration': duration,
            'src_bytes': src_bytes,
            'dst_bytes': dst_bytes,
            'failed_logins': failed_logins,
            'protocol_type_encoded': protocol_encoded,
            'count': count
        }])
        
        prediction = self.model.predict(input_data)[0]
        probability = self.model.predict_proba(input_data)[0][1]
        
        return prediction, probability
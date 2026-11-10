# Añade esta importación arriba:
import joblib

class IDSEngine:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.protocol_encoder = LabelEncoder()
        self.is_trained = False
        self.model_path = "ids_model.joblib" # Archivo donde guardaremos el cerebro

    def train(self, filepath):
        """Entrena el modelo y lo guarda en disco."""
        # Si el modelo ya existe, lo cargamos y no re-entrenamos
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            return 1.0, "Model loaded from disk." # Retornamos 100% por ser cargado

        # Si no existe, entrenamos normal
        X, y = self.load_and_prepare_data(filepath)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # GUARDAMOS EL MODELO EN EL DISCO
        joblib.dump(self.model, self.model_path)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy, classification_report(y_test, y_pred)
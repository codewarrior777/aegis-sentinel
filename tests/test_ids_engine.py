import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ids_engine import IDSEngine

@pytest.fixture
def engine():
    return IDSEngine()

def test_model_training_and_saving(engine):
    dataset_path = os.path.join(os.path.dirname(__file__), "../network_traffic.csv")
    if not os.path.exists(dataset_path):
        from src.data_generator import generate_traffic_data
        generate_traffic_data()
        
    accuracy, report = engine.train(dataset_path)
    assert engine.is_trained == True
    assert os.path.exists(engine.model_path) == True

def test_predict_attack(engine):
    engine.train(os.path.join(os.path.dirname(__file__), "../network_traffic.csv"))
    prediction, probability = engine.predict(
        duration=0.1, src_bytes=50, dst_bytes=20, 
        failed_logins=50, protocol_type="TCP", count=500
    )
    assert prediction == 1
    assert probability > 0.5

def test_predict_normal(engine):
    engine.train(os.path.join(os.path.dirname(__file__), "../network_traffic.csv"))
    prediction, probability = engine.predict(
        duration=10.0, src_bytes=500, dst_bytes=1000, 
        failed_logins=0, protocol_type="TCP", count=1
    )
    assert prediction == 0
    assert probability < 0.5
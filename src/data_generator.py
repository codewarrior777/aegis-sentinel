"""
Network Traffic Data Generator for Aegis-Sentinel.
Simulates normal traffic and cyber attacks (DDoS, Brute Force) to train the AI.
"""

import pandas as pd
import numpy as np
import os

def generate_traffic_data(num_samples=5000):
    np.random.seed(42)
    
    # 1. Generar Tráfico Normal (Label: 0)
    normal_data = {
        "duration": np.random.exponential(scale=10, size=int(num_samples * 0.7)),
        "src_bytes": np.random.normal(loc=500, scale=100, size=int(num_samples * 0.7)),
        "dst_bytes": np.random.normal(loc=1000, scale=200, size=int(num_samples * 0.7)),
        "failed_logins": np.random.poisson(lam=0.1, size=int(num_samples * 0.7)),
        "protocol_type": np.random.choice(["TCP", "UDP", "ICMP"], p=[0.8, 0.15, 0.05], size=int(num_samples * 0.7)),
        "count": np.random.randint(1, 10, size=int(num_samples * 0.7)),
        "class": [0] * int(num_samples * 0.7)
    }
    
    # 2. Generar Tráfico Malicioso (Label: 1)
    attack_data = {
        "duration": np.random.exponential(scale=2, size=int(num_samples * 0.3)),
        "src_bytes": np.random.normal(loc=100, scale=50, size=int(num_samples * 0.3)),
        "dst_bytes": np.random.normal(loc=50, scale=20, size=int(num_samples * 0.3)),
        "failed_logins": np.random.poisson(lam=5.0, size=int(num_samples * 0.3)),
        "protocol_type": np.random.choice(["TCP", "UDP", "ICMP"], p=[0.95, 0.01, 0.04], size=int(num_samples * 0.3)),
        "count": np.random.randint(50, 200, size=int(num_samples * 0.3)),
        "class": [1] * int(num_samples * 0.3)
    }
    
    # Crear DataFrames
    df_normal = pd.DataFrame(normal_data)
    df_attack = pd.DataFrame(attack_data)
    
    # Unir y mezclar los datos
    df = pd.concat([df_normal, df_attack]).sample(frac=1).reset_index(drop=True)
    
    # Limpiar valores (asegurar que no haya negativos en bytes/tiempo)
    df["duration"] = df["duration"].abs()
    df["src_bytes"] = df["src_bytes"].abs().round()
    df["dst_bytes"] = df["dst_bytes"].abs().round()
    
    # Guardar el archivo CSV en la raíz del proyecto
    output_path = os.path.join(os.path.dirname(__file__), "../network_traffic.csv")
    df.to_csv(output_path, index=False)
    
    print(f"✅ Dataset generado exitosamente con {len(df)} registros.")
    print(f"📁 Guardado en: {output_path}")
    print("\nPrimeras 5 filas del dataset:")
    print(df.head())

if __name__ == "__main__":
    generate_traffic_data()
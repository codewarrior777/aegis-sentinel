"""
Aegis-Sentinel: AI Network Intrusion Detection System.
Tactical Dashboard UI - Neon Blue Theme.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from src.ids_engine import IDSEngine
from src.data_generator import generate_traffic_data

st.set_page_config(page_title="Aegis Sentinel", page_icon="🪖", layout="wide")

# ==========================================
# 🎨 NEON BLUE THEME (CSS)
# ==========================================
neon_blue_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

/* Fondo general azul muy oscuro con cuadrícula cian */
.stApp {
    background-color: #030b17;
    background-image: 
        linear-gradient(rgba(0, 243, 255, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 243, 255, 0.05) 1px, transparent 1px);
    background-size: 30px 30px;
    color: #a0d8ef;
    font-family: 'Share Tech Mono', monospace;
}

/* Título principal en Azul Neón con borde púrpura */
h1 {
    color: #00f3ff !important;
    text-shadow: 0 0 10px rgba(0, 243, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 2px solid #8a2be2;
    padding-bottom: 10px;
}

/* Subtítulos en Azul Claro */
h2, h3 {
    color: #00d4ff !important;
    text-transform: uppercase;
}

/* Botones Estilo Cyberpunk */
.stButton > button {
    background-color: #051024 !important;
    color: #00f3ff !important;
    border: 1px solid #00f3ff !important;
    border-radius: 0px !important;
    text-transform: uppercase;
    transition: all 0.2s ease !important;
    width: 100%;
    box-shadow: 0 0 5px rgba(0, 243, 255, 0.2);
}

.stButton > button:hover {
    background-color: #00f3ff !important;
    color: #000 !important;
    box-shadow: 0 0 20px rgba(0, 243, 255, 0.8) !important;
}

/* Tarjetas de métricas */
div[data-testid="stMetric"] {
    background-color: #051024;
    border: 1px solid #1a3b5c;
    border-top: 3px solid #8a2be2;
    border-radius: 0px;
    padding: 15px;
}
div[data-testid="stMetricValue"] {
    color: #00f3ff !important;
}

/* Barra lateral */
.stSidebar .stAlert {
    background-color: #051024;
    border: 1px solid #8a2be2;
    color: #00f3ff;
}
</style>
"""
st.markdown(neon_blue_css, unsafe_allow_html=True)

# ==========================================
# SIDEBAR DISCLAIMER
# ==========================================
st.sidebar.warning(
    "⚠️ **RESTRICTED SYSTEM**\n\n"
    "This is a simulated Network Intrusion Detection System (IDS). "
    "The AI is trained on synthetic data for educational and portfolio purposes. "
    "Do not use this as a replacement for a real enterprise firewall."
)

# ==========================================
# MODEL LOADING
# ==========================================
@st.cache_resource
def load_model():
    engine = IDSEngine()
    dataset_path = os.path.join(os.path.dirname(__file__), "network_traffic.csv")
    
    if not os.path.exists(dataset_path):
        generate_traffic_data()
        
    if os.path.exists(dataset_path):
        engine.train(dataset_path)
    return engine

try:
    ids_engine = load_model()
    model_ready = True
except Exception as e:
    st.error(f"Failed to load AI model. Error: {e}")
    model_ready = False

# ==========================================
# HEADER
# ==========================================
st.title("🪖 AEGIS-SENTINEL // NIDS")
st.markdown("**AI-Powered Network Intrusion Detection System**")
st.divider()

# ==========================================
# LAYOUT: INPUT & RESULTS
# ==========================================
col_input, col_output = st.columns([1, 1.5], gap="large")

with col_input:
    st.markdown("### 📡 Connection Telemetry")
    st.write("Input the network connection parameters to analyze.")
    
    duration = st.number_input("Duration (seconds)", min_value=0.0, value=10.0, step=0.1)
    src_bytes = st.number_input("Source Bytes", min_value=0, value=500)
    dst_bytes = st.number_input("Destination Bytes", min_value=0, value=1000)
    failed_logins = st.number_input("Failed Logins", min_value=0, value=0)
    protocol = st.selectbox("Protocol Type", ["TCP", "UDP", "ICMP"])
    count = st.number_input("Connection Count (to same host)", min_value=1, value=1)
    
    scan_btn = st.button("🚀 INITIATE DEEP PACKET INSPECTION", type="primary")

with col_output:
    st.markdown("### 🖥️ Threat Analysis")
    
    if scan_btn and model_ready:
        # Run prediction
        prediction, probability = ids_engine.predict(
            duration, src_bytes, dst_bytes, failed_logins, protocol, count
        )
        
        # Gauge Chart for Threat Probability (Neon Blue Theme)
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = probability * 100,
            title = {'text': "Threat Level (%)", 'font': {'color': '#00f3ff', 'family': 'Share Tech Mono'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#00f3ff"},
                'bar': {'color': "#ff003c" if prediction == 1 else "#00f3ff"}, # Rojo si es ataque, Cian si es normal
                'bgcolor': "#051024",
                'borderwidth': 2,
                'bordercolor': "#1a3b5c",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(0, 243, 255, 0.2)'},   # Cian bajo
                    {'range': [40, 70], 'color': 'rgba(138, 43, 226, 0.2)'}, # Púrpura medio
                    {'range': [70, 100], 'color': 'rgba(255, 0, 60, 0.2)'}], # Rojo alto
                'threshold': {
                    'line': {'color': "#ff003c", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}
            }
        ))
        fig.update_layout(
            paper_bgcolor="#030b17",
            font={'color': "#a0d8ef", 'family': 'Share Tech Mono'},
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig, width="stretch")
        
        # Results output
        if prediction == 1:
            st.error(f"🚨 **INTRUSION DETECTED!** (Confidence: {probability*100:.2f}%)")
            st.markdown("""
            **Analysis:** The AI has classified this connection as malicious. 
            High failed logins or abnormal connection counts indicate a Brute Force or DDoS attempt. 
            **Action:** Drop packet and block source IP.
            """)
        else:
            st.success(f"✅ **Connection Normal** (Anomaly Prob: {probability*100:.2f}%)")
            st.markdown("""
            **Analysis:** The AI has classified this connection as benign.
            The traffic patterns match normal user behavior.
            **Action:** Allow traffic.
            """)
    else:
        st.info("💡 **STANDBY MODE:** Awaiting network telemetry to begin AI inspection.")
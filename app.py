"""
Aegis-Sentinel: AI Network Intrusion Detection System.
Tactical Dashboard UI.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from src.ids_engine import IDSEngine

st.set_page_config(page_title="Aegis Sentinel", page_icon="🪖", layout="wide")

# ==========================================
# 🎨 CYBERPUNK MILITARY THEME (CSS)
# ==========================================
military_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.stApp {
    background-color: #0a0a0f;
    background-image: 
        linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
    background-size: 30px 30px;
    color: #e0e0e0;
    font-family: 'Share Tech Mono', monospace;
}

h1 {
    color: #00ff41 !important;
    text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 2px solid #ff4c00;
    padding-bottom: 10px;
}

h2, h3 {
    color: #00ff41 !important;
    text-transform: uppercase;
}

.stButton > button {
    background-color: #111 !important;
    color: #00ff41 !important;
    border: 1px solid #00ff41 !important;
    border-radius: 0px !important;
    text-transform: uppercase;
    transition: all 0.2s ease !important;
    width: 100%;
}

.stButton > button:hover {
    background-color: #00ff41 !important;
    color: #000 !important;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.5) !important;
}

div[data-testid="stMetric"] {
    background-color: #111;
    border: 1px solid #333;
    border-top: 3px solid #ff4c00;
    border-radius: 0px;
    padding: 15px;
}
div[data-testid="stMetricValue"] {
    color: #00ff41 !important;
}
</style>
"""
st.markdown(military_css, unsafe_allow_html=True)

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
# MODEL LOADING (Cache it)
# ==========================================
@st.cache_resource
def load_model():
    engine = IDSEngine()
    # Busca el CSV en la raíz del proyecto
    dataset_path = os.path.join(os.path.dirname(__file__), "network_traffic.csv")
    if os.path.exists(dataset_path):
        engine.train(dataset_path)
    return engine

try:
    ids_engine = load_model()
    model_ready = True
except Exception as e:
    st.error(f"Failed to load AI model. Ensure `network_traffic.csv` exists in the root directory. Error: {e}")
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
        
        # Gauge Chart for Threat Probability
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = probability * 100,
            title = {'text': "Threat Level (%)", 'font': {'color': '#00ff41', 'family': 'Share Tech Mono'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#00ff41"},
                'bar': {'color': "#ff4c00" if prediction == 1 else "#00ff41"},
                'bgcolor': "#111",
                'borderwidth': 2,
                'bordercolor': "#333",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(0, 255, 65, 0.2)'},
                    {'range': [40, 70], 'color': 'rgba(255, 255, 0, 0.2)'},
                    {'range': [70, 100], 'color': 'rgba(255, 76, 0, 0.2)'}],
                'threshold': {
                    'line': {'color': "#ff4c00", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}
            }
        ))
        fig.update_layout(
            paper_bgcolor="#0a0a0f",
            font={'color': "#e0e0e0", 'family': 'Share Tech Mono'},
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        # FIX aplicado: width="stretch"
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
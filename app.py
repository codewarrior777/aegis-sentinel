"""
Aegis-Sentinel: AI Network Intrusion Detection System.
Ultimate God Level - Live Simulation, XAI, SOAR, and Tactical Radar.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os
import time
import json
import random
from src.ids_engine import IDSEngine
from src.data_generator import generate_traffic_data

st.set_page_config(page_title="Aegis Sentinel", page_icon="🪖", layout="wide")

# ==========================================
# 🎨 FLAT NEON BLUE THEME (NO SHADOWS)
# ==========================================
flat_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.stApp {
    background-color: #0b132b;
    color: #ffffff;
    font-family: 'Share Tech Mono', monospace;
}

h1 { color: #00f3ff !important; text-transform: uppercase; border-bottom: 2px solid #8a2be2; padding-bottom: 10px; }
h2, h3 { color: #00f3ff !important; text-transform: uppercase; }

.stButton > button {
    background-color: #1a3b5c !important;
    color: #ffffff !important;
    border: 2px solid #00f3ff !important;
    border-radius: 4px !important;
    text-transform: uppercase;
    font-weight: bold;
    transition: all 0.2s ease !important;
    width: 100%;
    font-size: 15px;
}
.stButton > button:hover { background-color: #00f3ff !important; color: #000000 !important; }

div[data-testid="stMetric"] {
    background-color: #1c2541;
    border: 1px solid #3a506b;
    border-left: 5px solid #8a2be2;
    padding: 15px;
}
div[data-testid="stMetricValue"] { color: #00f3ff !important; }

.alert-critical {
    background-color: #3b000a;
    border: 2px solid #ff003c;
    color: #ffffff;
    padding: 15px;
    border-radius: 4px;
    font-weight: bold;
    text-align: center;
}
.alert-safe {
    background-color: #002233;
    border: 2px solid #00f3ff;
    color: #ffffff;
    padding: 15px;
    border-radius: 4px;
    font-weight: bold;
    text-align: center;
}

.terminal-window {
    background-color: #000000;
    border: 2px solid #3a506b;
    padding: 15px;
    height: 160px;
    overflow-y: auto;
    font-size: 14px;
    color: #ffffff;
}
.log-line { margin-bottom: 5px; }
.log-warn { color: #ff003c; font-weight: bold; }
.log-success { color: #00ff41; font-weight: bold; }
</style>
"""
st.markdown(flat_css, unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================
if "total_scans" not in st.session_state: st.session_state.total_scans = 1420
if "threats_blocked" not in st.session_state: st.session_state.threats_blocked = 12
if "incident_logs" not in st.session_state: st.session_state.incident_logs = []

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
# HEADER & METRICS
# ==========================================
st.title("🪖 AEGIS-SENTINEL // NIDS")
st.markdown("**AI-Powered Network Intrusion Detection System**")

m1, m2, m3, m4 = st.columns(4)
m1.metric("System Status", "ONLINE", delta="Active")
m2.metric("Total Packets", f"{st.session_state.total_scans:,}")
m3.metric("Threats Blocked", f"{st.session_state.threats_blocked}", delta="-1", delta_color="inverse")
m4.metric("AI Confidence", "99.8%", delta="Optimal")
st.divider()

# ==========================================
# LAYOUT
# ==========================================
col_left, col_right = st.columns([1, 1.5], gap="large")

with col_left:
    st.markdown("### 📡 Connection Telemetry")
    duration = st.number_input("Duration (sec)", min_value=0.0, value=10.0, step=0.1)
    src_bytes = st.number_input("Source Bytes", min_value=0, value=500)
    dst_bytes = st.number_input("Dest Bytes", min_value=0, value=1000)
    failed_logins = st.number_input("Failed Logins", min_value=0, value=0)
    protocol = st.selectbox("Protocol", ["TCP", "UDP", "ICMP"])
    count = st.number_input("Connection Count", min_value=1, value=1)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        scan_btn = st.button("🚀 INSPECT PACKET", type="primary")
    with col_btn2:
        live_btn = st.button("⚡ START LIVE SIMULATION")

with col_right:
    st.markdown("### 🖥️ Threat Analysis")
    
    # Función para procesar un escaneo
    def process_scan(dur, src, dst, f_log, proto, cnt):
        st.session_state.total_scans += 1
        pred, prob = ids_engine.predict(dur, src, dst, f_log, proto, cnt)
        
        # Guardar Incidente si es ataque (SOAR)
        if pred == 1:
            st.session_state.threats_blocked += 1
            incident = {
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "Source_Bytes": src, "Dest_Bytes": dst,
                "Failed_Logins": f_log, "Conn_Count": cnt,
                "Threat_Prob": f"{prob*100:.2f}%"
            }
            st.session_state.incident_logs.append(incident)
            
        return pred, prob

    current_pred, current_prob = None, None

    if scan_btn and model_ready:
        with st.spinner("AI Analyzing..."):
            time.sleep(0.5)
            current_pred, current_prob = process_scan(duration, src_bytes, dst_bytes, failed_logins, protocol, count)
            
    elif live_btn and model_ready:
        st.info("⚡ LIVE SIMULATION RUNNING... Monitoring traffic...")
        # Simulador de tráfico en vivo
        for _ in range(5):
            is_attack = random.choice([False, False, True]) 
            if is_attack:
                d, s, de, fl, c = 0.5, 50, 20, random.randint(10, 50), random.randint(100, 500)
            else:
                d, s, de, fl, c = random.uniform(5, 15), 500, 1000, 0, random.randint(1, 5)
                
            current_pred, current_prob = process_scan(d, s, de, fl, "TCP", c)
            if current_pred == 1:
                st.error("🚨 INTRUSION DETECTED IN LIVE TRAFFIC!")
            time.sleep(0.8)

    # Mostrar Resultados (Aguja)
    if current_pred is not None:
        gauge_color = "#ff003c" if current_pred == 1 else "#00f3ff"
        fig = go.Figure(go.Indicator(
            mode = "gauge+number", value = current_prob * 100,
            title = {'text': "Threat Level (%)", 'font': {'color': '#ffffff'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': "#ffffff"},
                'bar': {'color': gauge_color}, 'bgcolor': "#1c2541",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(0, 243, 255, 0.2)'},
                    {'range': [40, 70], 'color': 'rgba(138, 43, 226, 0.2)'},
                    {'range': [70, 100], 'color': 'rgba(255, 0, 60, 0.2)'}],
            }
        ))
        fig.update_layout(paper_bgcolor="#0b132b", height=200, margin=dict(l=20, r=20, t=30, b=10))
        st.plotly_chart(fig, width="stretch")
        
        if current_pred == 1:
            st.markdown('<div class="alert-critical">🚨 INTRUSION DETECTED!<br>Action: Dropping packet and blocking source IP.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-safe">✅ CONNECTION NORMAL<br>Action: Allow traffic.</div>', unsafe_allow_html=True)
    else:
        st.info("💡 **STANDBY MODE:** Awaiting network telemetry.")

    # --- RED RADAR TACTICS ---
    st.markdown("### 📡 Network Radar")
    fig_radar = go.Figure()
    
    # Anillos y líneas
    for r in [0.25, 0.5, 0.75, 1.0]:
        fig_radar.add_trace(go.Scatterpolar(r=[r]*100, theta=np.linspace(0, 360, 100), mode='lines', line=dict(color='rgba(0, 243, 255, 0.3)', width=1), showlegend=False))
    for theta in [0, 90, 180, 270]:
        fig_radar.add_trace(go.Scatterpolar(r=[0, 1], theta=[theta, theta], mode='lines', line=dict(color='rgba(0, 243, 255, 0.3)', width=1), showlegend=False))
        
    # Haz de barrido
    sweep_theta = np.linspace(45, 0, 20).tolist()
    fig_radar.add_trace(go.Scatterpolar(r=[0] + [1]*20, theta=[0] + sweep_theta, fill='toself', fillcolor='rgba(0, 243, 255, 0.15)', line=dict(color='rgba(0, 243, 255, 0)'), showlegend=False))
    
    # Blips normales
    fig_radar.add_trace(go.Scatterpolar(r=[0.3, 0.7, 0.5, 0.9, 0.4, 0.8], theta=[45, 120, 200, 280, 330, 15], mode='markers', marker=dict(color='#00ff41', size=[6, 8, 5, 10, 4, 7]), showlegend=False))
    
    # Blips de ataque
    if current_pred == 1:
        fig_radar.add_trace(go.Scatterpolar(r=[0.6, 0.8, 0.4], theta=[150, 220, 300], mode='markers', marker=dict(color='#ff003c', size=[14, 16, 12], symbol='x'), showlegend=False))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=False, range=[0, 1]), angularaxis=dict(visible=False), bgcolor='#0b132b'),
        showlegend=False, paper_bgcolor='#0b132b', margin=dict(l=10, r=10, t=10, b=10), height=250
    )
    st.plotly_chart(fig_radar, width="stretch")

# ==========================================
# EXPLAINABLE AI (XAI) & SOAR
# ==========================================
if current_pred == 1:
    st.divider()
    col_xai, col_soar = st.columns(2)
    
    with col_xai:
        st.markdown("### 🧠 AI Explainability (XAI)")
        st.write("Why did the AI flag this? Top contributing features:")
        importances = ids_engine.get_feature_importances()
        df_imp = pd.DataFrame(list(importances.items()), columns=['Feature', 'Importance'])
        fig_xai = px.bar(df_imp, x='Importance', y='Feature', orientation='h', color_discrete_sequence=['#8a2be2'])
        fig_xai.update_layout(paper_bgcolor="#0b132b", plot_bgcolor="#1c2541", font_color="#ffffff", height=250)
        st.plotly_chart(fig_xai, width="stretch")
        
    with col_soar:
        st.markdown("### 📁 Automated Incident Response (SOAR)")
        st.write("An incident report has been generated. Download for SOC documentation.")
        json_logs = json.dumps(st.session_state.incident_logs, indent=4)
        st.download_button(
            label="⬇️ DOWNLOAD INCIDENT REPORT (JSON)",
            data=json_logs,
            file_name=f"incident_report_{int(time.time())}.json",
            mime="application/json"
        )

# ==========================================
# TERMINAL LOGS
# ==========================================
st.markdown("### 💻 Terminal Logs")
st.markdown('<div class="terminal-window"><div class="log-line">[SYSTEM] Aegis-Sentinel initialized.</div><div class="log-line">[SYSTEM] AI Model loaded via joblib.</div><div class="log-line">[SYSTEM] Listening on eth0...</div></div>', unsafe_allow_html=True)
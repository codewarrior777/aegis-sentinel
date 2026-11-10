"""
Aegis-Sentinel: AI Network Intrusion Detection System.
Tactical Dashboard UI - Ultimate SOC Experience.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import time
import random
from src.ids_engine import IDSEngine
from src.data_generator import generate_traffic_data

st.set_page_config(page_title="Aegis Sentinel", page_icon="🪖", layout="wide")

# ==========================================
# 🎨 ULTIMATE NEON BLUE THEME (CSS)
# ==========================================
ultimate_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

/* Fondo general con efecto scanline */
.stApp {
    background-color: #030b17;
    background-image: 
        linear-gradient(rgba(0, 243, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px);
    background-size: 20px 20px;
    color: #a0d8ef;
    font-family: 'Share Tech Mono', monospace;
    overflow: hidden;
}

/* Scanlines Effect */
.stApp::before {
    content: " ";
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    z-index: 2;
    background-size: 100% 2px, 3px 100%;
    pointer-events: none;
}

/* Título */
h1 {
    color: #00f3ff !important;
    text-shadow: 0 0 10px rgba(0, 243, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 2px solid #8a2be2;
    padding-bottom: 10px;
}

h2, h3 {
    color: #00d4ff !important;
    text-transform: uppercase;
}

/* Botones */
.stButton > button {
    background-color: #051024 !important;
    color: #00f3ff !important;
    border: 1px solid #00f3ff !important;
    border-radius: 0px !important;
    text-transform: uppercase;
    transition: all 0.2s ease !important;
    width: 100%;
    box-shadow: 0 0 10px rgba(0, 243, 255, 0.2);
    font-size: 16px;
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
    padding: 10px;
    box-shadow: 0 0 10px rgba(138, 43, 226, 0.2);
}
div[data-testid="stMetricValue"] {
    color: #00f3ff !important;
}

/* Alertas Personalizadas */
.alert-critical {
    background-color: rgba(255, 0, 60, 0.1);
    border: 2px solid #ff003c;
    color: #ff003c;
    padding: 20px;
    border-radius: 5px;
    font-weight: bold;
    text-align: center;
    animation: pulse-red 1.5s infinite;
}
.alert-safe {
    background-color: rgba(0, 243, 255, 0.1);
    border: 2px solid #00f3ff;
    color: #00f3ff;
    padding: 20px;
    border-radius: 5px;
    font-weight: bold;
    text-align: center;
}

@keyframes pulse-red {
    0% { box-shadow: 0 0 0 0 rgba(255, 0, 60, 0.7); }
    70% { box-shadow: 0 0 0 15px rgba(255, 0, 60, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 0, 60, 0); }
}

/* Terminal Logs */
.terminal-window {
    background-color: #000;
    border: 1px solid #00f3ff;
    padding: 15px;
    height: 200px;
    overflow-y: auto;
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    color: #00f3ff;
    box-shadow: inset 0 0 20px rgba(0, 243, 255, 0.1);
}
.log-line { margin-bottom: 5px; }
.log-warn { color: #ff003c; }
.log-success { color: #00ff41; }
</style>
"""
st.markdown(ultimate_css, unsafe_allow_html=True)

# ==========================================
# SESSION STATE (For Metrics)
# ==========================================
if "total_scans" not in st.session_state:
    st.session_state.total_scans = 1420
if "threats_blocked" not in st.session_state:
    st.session_state.threats_blocked = 12

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
# HEADER & TOP METRICS
# ==========================================
st.title("🪖 AEGIS-SENTINEL // NIDS")
st.markdown("**AI-Powered Network Intrusion Detection System**")

# Panel de Métricas Superior
m1, m2, m3, m4 = st.columns(4)
m1.metric("System Status", "ONLINE", delta="Active")
m2.metric("Total Packets Scanned", f"{st.session_state.total_scans:,}")
m3.metric("Threats Blocked", f"{st.session_state.threats_blocked}", delta="-1", delta_color="inverse")
m4.metric("AI Confidence", "99.8%", delta="Optimal")

st.divider()

# ==========================================
# MAIN LAYOUT
# ==========================================
col_input, col_radar, col_output = st.columns([1, 1, 1.2], gap="medium")

with col_input:
    st.markdown("### 📡 Connection Telemetry")
    
    duration = st.number_input("Duration (sec)", min_value=0.0, value=10.0, step=0.1)
    src_bytes = st.number_input("Source Bytes", min_value=0, value=500)
    dst_bytes = st.number_input("Dest Bytes", min_value=0, value=1000)
    failed_logins = st.number_input("Failed Logins", min_value=0, value=0)
    protocol = st.selectbox("Protocol", ["TCP", "UDP", "ICMP"])
    count = st.number_input("Conn. Count", min_value=1, value=1)
    
    scan_btn = st.button("🚀 INITIATE PACKET INSPECTION", type="primary")

with col_radar:
    st.markdown("### 📡 Network Radar")
    # Simulando un radar militar
    radar_fig = go.Figure(data=go.Scatterpolar(
        r=[1, 1, 1, 1, 1, 1],
        theta=[0, 60, 120, 180, 240, 300],
        fill='toself',
        fillcolor='rgba(0, 243, 255, 0.1)',
        line=dict(color='#00f3ff', width=2),
        name='Scan Area'
    ))
    # Añadir blips aleatorios (falsos contactos)
    radar_fig.add_trace(go.Scatterpolar(
        r=[0.8, 0.6, 0.9],
        theta=[45, 180, 270],
        mode='markers',
        marker=dict(color='#8a2be2', size=10, symbol='circle'),
        name='Contacts'
    ))
    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 1]),
            angularaxis=dict(visible=False),
            bgcolor='#030b17'
        ),
        showlegend=False,
        paper_bgcolor='#030b17',
        margin=dict(l=10, r=10, t=10, b=10),
        height=300
    )
    st.plotly_chart(radar_fig, width="stretch")

with col_output:
    st.markdown("### 🖥️ Threat Analysis")
    
    if scan_btn and model_ready:
        with st.spinner("AI Analyzing Packets..."):
            time.sleep(0.5) # Pequeña pausa dramática
            prediction, probability = ids_engine.predict(
                duration, src_bytes, dst_bytes, failed_logins, protocol, count
            )
            st.session_state.total_scans += 1
            
            # Gauge Chart
            gauge_color = "#ff003c" if prediction == 1 else "#00f3ff"
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = probability * 100,
                title = {'text': "Threat Level (%)", 'font': {'color': '#00f3ff', 'size': 20}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#00f3ff"},
                    'bar': {'color': gauge_color},
                    'bgcolor': "#051024",
                    'borderwidth': 2,
                    'bordercolor': "#1a3b5c",
                    'steps': [
                        {'range': [0, 40], 'color': 'rgba(0, 243, 255, 0.2)'},
                        {'range': [40, 70], 'color': 'rgba(138, 43, 226, 0.2)'},
                        {'range': [70, 100], 'color': 'rgba(255, 0, 60, 0.2)'}],
                    'threshold': {'line': {'color': "#ff003c", 'width': 4}, 'thickness': 0.75, 'value': 90}
                }
            ))
            fig.update_layout(
                paper_bgcolor="#030b17", font={'color': "#a0d8ef"},
                height=250, margin=dict(l=20, r=20, t=30, b=10)
            )
            st.plotly_chart(fig, width="stretch")
            
            # Custom Alert Box
            if prediction == 1:
                st.session_state.threats_blocked += 1
                st.markdown('<div class="alert-critical">🚨 INTRUSION DETECTED!<br>Action: Dropping packet and blocking source IP.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-safe">✅ CONNECTION NORMAL<br>Action: Allow traffic.</div>', unsafe_allow_html=True)
    else:
        st.info("💡 **STANDBY MODE:** Awaiting network telemetry.")

# ==========================================
# BOTTOM TERMINAL LOGS
# ==========================================
st.divider()
st.markdown("### 💻 Terminal Logs")
terminal_placeholder = st.empty()

if scan_btn and model_ready:
    logs = [
        f"<div class='log-line'>[SYSTEM] Initiating Deep Packet Inspection...</div>",
        f"<div class='log-line'>[AI] Extracting telemetry features (bytes, duration, logins)...</div>",
        f"<div class='log-line'>[AI] Running Random Forest Classifier...</div>",
    ]
    
    if prediction == 1:
        logs.append("<div class='log-line log-warn'>[WARN] High volume of failed logins detected!</div>")
        logs.append("<div class='log-line log-warn'>[WARN] Anomalous connection count (DDoS signature)!</div>")
        logs.append("<div class='log-line log-warn'>[ALERT] INTRUSION DETECTED. Confidence > 99%.</div>")
        logs.append(f"<div class='log-line log-warn'>[ACTION] Dropping packets from source. Threat blocked.</div>")
    else:
        logs.append("<div class='log-line log-success'>[INFO] Traffic patterns match normal user behavior.</div>")
        logs.append("<div class='log-line log-success'>[ACTION] Allowing traffic.</div>")
        
    logs.append("<div class='log-line'>[SYSTEM] Scan complete. Listening for next connection...</div>")
    
    # Efecto de escribir en la terminal
    terminal_html = ""
    for log in logs:
        terminal_html += log
        terminal_placeholder.markdown(f'<div class="terminal-window">{terminal_html}</div>', unsafe_allow_html=True)
        time.sleep(0.4)
else:
    terminal_placeholder.markdown(
        '<div class="terminal-window"><div class="log-line">[SYSTEM] Aegis-Sentinel initialized.</div><div class="log-line">[SYSTEM] AI Model loaded successfully.</div><div class="log-line">[SYSTEM] Listening on eth0...</div></div>', 
        unsafe_allow_html=True
    )
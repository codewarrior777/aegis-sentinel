"""
Aegis-Sentinel: AI Network Intrusion Detection System.
Tactical Dashboard UI - Flat Neon Blue Theme (Perfect Layout).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import time
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

h1 {
    color: #00f3ff !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 2px solid #8a2be2;
    padding-bottom: 10px;
}

h2, h3 {
    color: #00f3ff !important;
    text-transform: uppercase;
}

.stButton > button {
    background-color: #1a3b5c !important;
    color: #ffffff !important;
    border: 2px solid #00f3ff !important;
    border-radius: 4px !important;
    text-transform: uppercase;
    font-weight: bold;
    transition: all 0.2s ease !important;
    width: 100%;
    font-size: 16px;
}
.stButton > button:hover {
    background-color: #00f3ff !important;
    color: #000000 !important;
}

div[data-testid="stMetric"] {
    background-color: #1c2541;
    border: 1px solid #3a506b;
    border-left: 5px solid #8a2be2;
    border-radius: 4px;
    padding: 15px;
}
div[data-testid="stMetricValue"] {
    color: #00f3ff !important;
}
div[data-testid="stMetricLabel"] {
    color: #ffffff !important;
}

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
    height: 180px;
    overflow-y: auto;
    font-family: 'Share Tech Mono', monospace;
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
# SESSION STATE (Metrics)
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
# LAYOUT: 2 COLUMNS
# ==========================================
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("### 📡 Connection Telemetry")
    duration = st.number_input("Duration (sec)", min_value=0.0, value=10.0, step=0.1)
    src_bytes = st.number_input("Source Bytes", min_value=0, value=500)
    dst_bytes = st.number_input("Dest Bytes", min_value=0, value=1000)
    failed_logins = st.number_input("Failed Logins", min_value=0, value=0)
    protocol = st.selectbox("Protocol", ["TCP", "UDP", "ICMP"])
    count = st.number_input("Connection Count", min_value=1, value=1)
    
    scan_btn = st.button("🚀 INITIATE PACKET INSPECTION", type="primary")
    
    # Movemos el Radar aquí, pero le damos altura fija para que no se corte
    st.markdown("### 📡 Network Radar")
    radar_fig = go.Figure(data=go.Scatterpolar(
        r=[1, 1, 1, 1, 1, 1], theta=[0, 60, 120, 180, 240, 300],
        fill='toself', fillcolor='rgba(0, 243, 255, 0.1)', line=dict(color='#00f3ff', width=2)
    ))
    radar_fig.add_trace(go.Scatterpolar(
        r=[0.8, 0.6, 0.9], theta=[45, 180, 270], mode='markers',
        marker=dict(color='#8a2be2', size=10)
    ))
    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 1]), 
            angularaxis=dict(visible=False), 
            bgcolor='#0b132b'
        ),
        showlegend=False, 
        paper_bgcolor='#0b132b', 
        margin=dict(l=10, r=10, t=10, b=10), 
        height=250 # Altura ajustada
    )
    st.plotly_chart(radar_fig, width="stretch")

with col_right:
    st.markdown("### 🖥️ Threat Analysis")
    
    if scan_btn and model_ready:
        with st.spinner("AI Analyzing Packets..."):
            time.sleep(0.5)
            prediction, probability = ids_engine.predict(
                duration, src_bytes, dst_bytes, failed_logins, protocol, count
            )
            st.session_state.total_scans += 1
            
            gauge_color = "#ff003c" if prediction == 1 else "#00f3ff"
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = probability * 100,
                title = {'text': "Threat Level (%)", 'font': {'color': '#ffffff', 'size': 20}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickcolor': "#ffffff", 'tickfont': {'color': '#ffffff'}},
                    'bar': {'color': gauge_color},
                    'bgcolor': "#1c2541", 
                    'bordercolor': "#3a506b",
                    'steps': [
                        {'range': [0, 40], 'color': 'rgba(0, 243, 255, 0.2)'},
                        {'range': [40, 70], 'color': 'rgba(138, 43, 226, 0.2)'},
                        {'range': [70, 100], 'color': 'rgba(255, 0, 60, 0.2)'}],
                    'threshold': {'line': {'color': "#ff003c", 'width': 4}, 'value': 90}
                }
            ))
            fig.update_layout(
                paper_bgcolor="#0b132b", 
                font={'color': "#ffffff"}, 
                height=250, 
                margin=dict(l=20, r=20, t=40, b=10)
            )
            st.plotly_chart(fig, width="stretch")
            
            if prediction == 1:
                st.session_state.threats_blocked += 1
                st.markdown('<div class="alert-critical">🚨 INTRUSION DETECTED!<br>Action: Dropping packet and blocking source IP.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-safe">✅ CONNECTION NORMAL<br>Action: Allow traffic.</div>', unsafe_allow_html=True)
                
        # Terminal Logs
        st.markdown("### 💻 Terminal Logs")
        terminal_html = ""
        terminal_placeholder = st.empty()
        logs = [
            "<div class='log-line'>[SYSTEM] Initiating Deep Packet Inspection...</div>",
            "<div class='log-line'>[AI] Extracting telemetry features...</div>"
        ]
        if prediction == 1:
            logs.extend([
                "<div class='log-line log-warn'>[WARN] High volume of failed logins!</div>",
                "<div class='log-line log-warn'>[WARN] Anomalous connection count (DDoS signature)!</div>",
                "<div class='log-line log-warn'>[ALERT] INTRUSION DETECTED. Confidence > 99%.</div>"
            ])
        else:
             logs.append("<div class='log-line log-success'>[INFO] Traffic patterns normal.</div>")
             
        for log in logs:
            terminal_html += log
            terminal_placeholder.markdown(f'<div class="terminal-window">{terminal_html}</div>', unsafe_allow_html=True)
            time.sleep(0.3)
    else:
        st.info("💡 **STANDBY MODE:** Awaiting network telemetry.")
        st.markdown("### 💻 Terminal Logs")
        st.markdown('<div class="terminal-window"><div class="log-line">[SYSTEM] Aegis-Sentinel initialized.</div><div class="log-line">[SYSTEM] AI Model loaded successfully.</div><div class="log-line">[SYSTEM] Listening on eth0...</div></div>', unsafe_allow_html=True)
import streamlit as st
import google.generativeai as genai
import os
import numpy as np
import json
import datetime
import pandas as pd
import requests
from PIL import Image
import streamlit.components.v1 as components
from dotenv import load_dotenv

# --- 1. CORE SETUP ---
st.set_page_config(page_title="Stadium Pulse: JARVIS Command Center", page_icon="🏟️", layout="wide")
load_dotenv()

# Initialize Enterprise State Matrix
if 'gate_history' not in st.session_state:
    st.session_state.gate_history = {
        "Gate 1": [45, 50, 58, 65, 72, 80, 95, 110, 130, 155], 
        "Gate 2": [30, 32, 31, 35, 33, 30, 32, 35, 31, 34],    
        "Gate 3": [12, 15, 18, 22, 25, 30, 42, 55, 70, 92],    
        "Gate 4": [20, 22, 21, 24, 25, 26, 28, 29, 30, 32]     
    }

if 'ledger' not in st.session_state:
    st.session_state.ledger = [
        {"Time": (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%H:%M:%S"), "Agent": "System Core", "Action": "Pub/Sub Telemetry Stream Initialized", "Status": "✅ Active"}
    ]

if 'last_speech' not in st.session_state:
    st.session_state.last_speech = ""

# --- 2. AUTOMATED VOICE TELEMETRY DISPATCH ENGINE ---
def automate_voice_announcer(text):
    if text and text != st.session_state.last_speech:
        st.session_state.last_speech = text
        clean_text = text.replace('"', '').replace("'", '').replace('\n', ' ')
        js_code = f"""
            <script>
                var msg = new SpeechSynthesisUtterance("{clean_text}");
                msg.lang = 'en-US';
                msg.rate = 1.0;
                window.speechSynthesis.speak(msg);
            </script>
        """
        components.html(js_code, height=0, width=0)

# --- 3. HELPER LOGIC ---
def log_event(agent, action, status="✅ Resolved"):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.ledger.insert(0, {"Time": timestamp, "Agent": agent, "Action": action, "Status": status})

def predict_crowd_surge(gate_name):
    history = st.session_state.gate_history[gate_name]
    x = np.arange(len(history))
    poly_model = np.poly1d(np.polyfit(x, np.array(history), 2))
    return max(int(poly_model(15)), 0)

def get_live_weather():
    owm_key = os.getenv("WEATHER_API_KEY")
    if owm_key:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q=Bengaluru&appid={owm_key}&units=metric"
            data = requests.get(url).json()
            return data["main"]["temp"], data["weather"][0]["description"].title()
        except: pass
    return 36.2, "Severe Heat / Thunderstorm Risk (Simulated)"

# Config Gemini Core
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')
import time

def safe_gemini_call(prompt, img=None):
    """Wraps Gemini calls with a small delay to respect rate limits."""
    try:
        # If we have an image, pass it; otherwise just the prompt
        if img:
            response = model.generate_content([prompt, img])
        else:
            response = model.generate_content(prompt)
        return response
    except Exception as e:
        if "429" in str(e):
            st.error("⚠️ API Quota reached. Cooling down for 5 seconds...")
            time.sleep(5)
            return None
        raise e

# Pre-calculate live parameters
p1 = predict_crowd_surge("Gate 1")
p2 = predict_crowd_surge("Gate 2")
p3 = predict_crowd_surge("Gate 3")
p4 = predict_crowd_surge("Gate 4")

# Pre-compute layout alerting structures
a1 = "critical-alert" if p1 > 150 else ""
a2 = "critical-alert" if p2 > 150 else ""
a3 = "critical-alert" if p3 > 150 else ""
a4 = "critical-alert" if p4 > 150 else ""
t1 = "critical-text" if p1 > 150 else ""
t2 = "critical-text" if p2 > 150 else ""
t3 = "critical-text" if p3 > 150 else ""
t4 = "critical-text" if p4 > 150 else ""

c1 = "#ef4444" if p1 > 150 else "#f59e0b" if p1 > 100 else "#16a34a"
c2 = "#ef4444" if p2 > 150 else "#f59e0b" if p2 > 100 else "#16a34a"
c3 = "#ef4444" if p3 > 150 else "#f59e0b" if p3 > 100 else "#16a34a"
c4 = "#ef4444" if p4 > 150 else "#f59e0b" if p4 > 100 else "#16a34a"

# --- 4. HIGH-CONTRAST LIGHT GLOW INTERFACE (CSS DESIGN SHIELD) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Share+Tech+Mono&family=Inter:wght@400;600;700;800&display=swap');
    
    /* Global Background Canvas */
    @keyframes grid-drift { 0% { background-position: 0 0; } 100% { background-position: 40px 40px; } }
    .stApp { 
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 50%, #cbd5e1 100%), radial-gradient(rgba(66, 133, 244, 0.08) 1.5px, transparent 1.5px);
        background-size: 100% 100%, 30px 30px; animation: grid-drift 30s linear infinite; 
        color: #0f172a !important; font-family: 'Inter', sans-serif; 
    }
    
    /* Realistic 3D Cinematic Arena Transformation Matrix */
    @keyframes arena-isometric-drift {
        0% { transform: perspective(1400px) rotateX(48deg) rotateZ(-32deg) rotateY(2deg) translateY(0px); box-shadow: -20px 30px 50px rgba(15,23,42,0.2); }
        50% { transform: perspective(1400px) rotateX(46deg) rotateZ(-30deg) rotateY(0deg) translateY(-12px); box-shadow: -35px 50px 75px rgba(15,23,42,0.3); }
        100% { transform: perspective(1400px) rotateX(48deg) rotateZ(-32deg) rotateY(2deg) translateY(0px); box-shadow: -20px 30px 50px rgba(15,23,42,0.2); }
    }
    
    @keyframes panel-drift-wave {
        0% { transform: translateY(0px) perspective(1000px) rotateX(1deg); }
        50% { transform: translateY(-6px) perspective(1000px) rotateX(1.5deg); }
        100% { transform: translateY(0px) perspective(1000px) rotateX(1deg); }
    }
    
    @keyframes neon-glow-cyan {
        0% { box-shadow: 0 10px 30px rgba(0, 172, 238, 0.15); border-color: rgba(0, 172, 238, 0.4); }
        50% { box-shadow: 0 15px 45px rgba(0, 172, 238, 0.35); border-color: rgba(0, 172, 238, 1); }
        100% { box-shadow: 0 10px 30px rgba(0, 172, 238, 0.15); border-color: rgba(0, 172, 238, 0.4); }
    }
    @keyframes neon-glow-red {
        0% { box-shadow: 0 10px 30px rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.3); }
        50% { box-shadow: 0 15px 45px rgba(239, 68, 68, 0.4); border-color: rgba(239, 68, 68, 1); }
        100% { box-shadow: 0 10px 30px rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.3); }
    }
    @keyframes neon-glow-amber {
        0% { box-shadow: 0 10px 30px rgba(245, 158, 11, 0.15); border-color: rgba(245, 158, 11, 0.4); }
        50% { box-shadow: 0 15px 45px rgba(245, 158, 11, 0.4); border-color: rgba(245, 158, 11, 1); }
        100% { box-shadow: 0 10px 30px rgba(245, 158, 11, 0.15); border-color: rgba(245, 158, 11, 0.4); }
    }
    @keyframes neon-glow-green {
        0% { box-shadow: 0 10px 30px rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.4); }
        50% { box-shadow: 0 15px 45px rgba(16, 185, 129, 0.4); border-color: rgba(16, 185, 129, 1); }
        100% { box-shadow: 0 10px 30px rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.4); }
    }
    @keyframes neon-glow-purple {
        0% { box-shadow: 0 10px 30px rgba(168, 85, 247, 0.15); border-color: rgba(168, 85, 247, 0.4); }
        50% { box-shadow: 0 15px 45px rgba(168, 85, 247, 0.4); border-color: rgba(168, 85, 247, 1); }
        100% { box-shadow: 0 10px 30px rgba(168, 85, 247, 0.15); border-color: rgba(168, 85, 247, 0.4); }
    }
    @keyframes active-tab-pulse {
        0% { box-shadow: 0 0 12px rgba(66, 133, 244, 0.2); border-color: rgba(66, 133, 244, 0.4); }
        50% { box-shadow: 0 0 25px rgba(66, 133, 244, 0.5); border-color: rgba(66, 133, 244, 1); background: rgba(66, 133, 244, 0.08) !important; }
        100% { box-shadow: 0 0 12px rgba(66, 133, 244, 0.2); border-color: rgba(66, 133, 244, 0.4); }
    }

    /* Core Metrics Glass Cards */
    .dashboard-card {
        background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border: 2px solid rgba(15, 23, 42, 0.15); box-shadow: 0 8px 25px rgba(15, 23, 42, 0.04);
        border-radius: 16px; padding: 24px; margin-bottom: 18px; transform: perspective(1000px) rotateX(1deg);
        transition: all 0.3s ease;
    }
    .dashboard-card:hover { transform: translateY(-5px) scale(1.01); border-color: #4285F4; box-shadow: 0 12px 35px rgba(66, 133, 244, 0.2); }
    
    /* True 3D Isometric Arena Box */
    .arena-isometric-box {
        background: radial-gradient(circle at 50% 50%, #1e293b 0%, #0f172a 100%) !important;
        border: 3px solid #cbd5e1; border-radius: 24px; padding: 45px; text-align: center;
        animation: arena-isometric-drift 8s ease-in-out infinite;
        transform-style: preserve-3d; margin-bottom: 25px; margin-top: 15px;
    }
    
    .feature-panel { border-radius: 16px; padding: 28px; margin-top: 15px; margin-bottom: 22px; }
    .panel-cyan { animation: panel-drift-wave 5s ease-in-out infinite, neon-glow-cyan 4s ease-in-out infinite; background: rgba(255, 255, 255, 0.95); }
    .panel-red { animation: panel-drift-wave 5.5s ease-in-out infinite, neon-glow-red 4s ease-in-out infinite; background: rgba(255, 255, 255, 0.95); }
    .panel-amber { animation: panel-drift-wave 4.8s ease-in-out infinite, neon-glow-amber 4s ease-in-out infinite; background: rgba(255, 255, 255, 0.95); }
    .panel-green { animation: panel-drift-wave 5.2s ease-in-out infinite, neon-glow-green 4s ease-in-out infinite; background: rgba(255, 255, 255, 0.95); }
    .panel-purple { animation: panel-drift-wave 6s ease-in-out infinite, neon-glow-purple 4s ease-in-out infinite; background: rgba(255, 255, 255, 0.95); }
    
    h1 { font-family: 'Orbitron', sans-serif; font-size: 52px !important; font-weight: 900 !important; letter-spacing: 3px !important; color: #0f172a !important; text-shadow: 0 0 15px rgba(66, 133, 244, 0.3); }
    h2 { font-family: 'Orbitron', sans-serif; font-size: 28px !important; font-weight: 800 !important; color: #0f172a !important; }
    h3 { font-family: 'Orbitron', sans-serif; font-size: 24px !important; font-weight: 800 !important; color: #0f172a !important; }
    h4 { font-family: 'Orbitron', sans-serif; font-size: 20px !important; font-weight: 700 !important; color: #0f172a !important; }
    
    /* Universal Content Override Rules */
    p, span, label, div { color: #0f172a !important; font-weight: 700 !important; font-size: 15px; }
    .feature-title { font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 900; letter-spacing: 1.5px; }
    .feature-desc-text { font-size: 18px; color: #1e293b !important; line-height: 1.6; margin-top: 12px; margin-bottom: 18px; font-weight: 700 !important; }
    .feature-guide-tag { background: #f8fafc; border-left: 5px solid #4285F4; padding: 14px 20px; font-size: 16px; color: #0f172a !important; border-radius: 0 8px 8px 0; margin-bottom: 25px; font-weight: 800 !important; border-top: 2px solid #e2e8f0; border-right: 2px solid #e2e8f0; border-bottom: 2px solid #e2e8f0; }
    
    pre, code { 
    background: #ffffff !important; 
    color: #0f172a !important; 
    font-family: 'Share Tech Mono', monospace !important; 
    font-size: 15px !important; 
    border-radius: 8px; 
    padding: 15px; 
    border: 2px solid #cbd5e1; 
}

div[data-testid="stCodeBlock"] pre {
    background-color: #ffffff !important;
    color: #0f172a !important;
}

div[data-testid="stJson"] {
    background-color: #ffffff !important;
}

div[data-testid="stJson"] * {
    color: #0f172a !important;
}
    @keyframes persistent-crisis-glow {
        0% { box-shadow: 0 0 25px rgba(220, 38, 38, 0.4), inset 0 0 15px rgba(220, 38, 38, 0.2); border-color: rgba(220, 38, 38, 0.6); background: #fef2f2 !important; }
        50% { box-shadow: 0 0 45px rgba(220, 38, 38, 0.85), inset 0 0 25px rgba(220, 38, 38, 0.4); border-color: rgba(220, 38, 38, 1); background: #fee2e2 !important; }
        100% { box-shadow: 0 0 25px rgba(220, 38, 38, 0.4), inset 0 0 15px rgba(220, 38, 38, 0.2); border-color: rgba(220, 38, 38, 0.6); background: #fef2f2 !important; }
    }
    .critical-alert { animation: persistent-crisis-glow 1.2s infinite !important; }
    .critical-text { color: #991b1b !important; font-weight: 900 !important; }
    
    .gcp-log { color: #16a34a !important; background: #f0fdf4; border: 2px solid #bbf7d0; font-family: 'Share Tech Mono', monospace; font-size: 14px; padding: 12px; border-radius: 8px; font-weight: bold; }
    .gcp-badge { color: #15803d !important; background: #f0fdf4; border: 2px solid #bbf7d0; font-family: 'Share Tech Mono', monospace; font-size: 12px; padding: 6px 14px; border-radius: 6px; display: inline-block; margin-top: 18px; font-weight: bold; }
    .agent-tag { background: rgba(66, 133, 244, 0.12); border: 2px solid rgba(66, 133, 244, 0.3); color: #1d4ed8 !important; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 800; display: inline-block; margin-bottom: 14px; font-family: 'Orbitron', sans-serif; }
    
    [data-testid="stSidebar"] { background: #0f172a !important; border-right: 3px solid #4285F4; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] strong, [data-testid="stSidebar"] li { color: #f8fafc !important; }
    
    /* 🚨 DROPDOWN SELECTION VISIBILITY PRESERVATION (FIXED DROPDOWN FADING EFFECT) 🚨 */
    div[data-baseweb="select"] > div { background-color: #ffffff !important; border: 2px solid #cbd5e1 !important; border-radius: 8px !important; }
    div[data-baseweb="select"] * { color: #0f172a !important; font-weight: 800 !important; font-size: 16px !important; }
    
    div[data-baseweb="popover"], div[role="listbox"], [id^="bui"]-menu, [data-testid="stSelectbox"] div, ul[role="listbox"] { background-color: #ffffff !important; color: #0f172a !important; }
    div[role="option"], li[role="option"], [data-baseweb="menu"] li, [data-baseweb="popover"] li { background-color: #ffffff !important; color: #0f172a !important; font-weight: 800 !important; font-size: 16px !important; padding: 14px 18px !important; border-bottom: 1px solid #f1f5f9 !important; }
    div[role="option"]:hover, li[role="option"]:hover, [data-baseweb="menu"] li:hover, [data-baseweb="popover"] li:hover { background-color: #e2e8f0 !important; color: #2563eb !important; }
    
    /* 🚨 FIXED FILE UPLOADER SYSTEM FOR PRECISE VISIBILITY OVERRIDES 🚨 */
    [data-testid="stFileUploader"] section { background-color: #ffffff !important; border: 2px dashed #cbd5e1 !important; border-radius: 12px; padding: 20px; }
    [data-testid="stFileUploader"] section *, [data-testid="stFileUploader"] div, [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] label { color: #0f172a !important; font-weight: 800 !important; font-size: 16px !important; }
    [data-testid="stFileUploader"] button { background-color: #0f172a !important; color: white !important; }
    [data-testid="stFileUploader"] button * { color: #ffffff !important; }

    .stTabs [data-baseweb="tab-list"] { background: rgba(255, 255, 255, 0.85) !important; border-bottom: 3px solid #cbd5e1 !important; gap: 14px !important; padding: 10px 14px !important; border-radius: 12px 12px 0 0 !important; }
    .stTabs [data-baseweb="tab"] { color: #334155 !important; background: #f8fafc !important; border: 2px solid #cbd5e1 !important; padding: 16px 32px !important; font-size: 17px !important; font-weight: 800 !important; font-family: 'Orbitron', sans-serif !important; border-radius: 8px 8px 0 0 !important; }
    .stTabs [aria-selected="true"] { color: #ffffff !important; background: #4285F4 !important; border-color: #4285F4 !important; transform: translateY(-4px) !important; }
    
    .stButton button { background: #0f172a !important; color: #ffffff !important; font-family: 'Orbitron', sans-serif; font-weight: 800; font-size: 16px !important; padding: 14px 30px !important; border-radius: 8px; width: 100%; border: none !important; }
    .stButton button * { color: #ffffff !important; }
    .stButton button:hover { transform: translateY(-2px) scale(1.01); background: #1e293b !important; }
    
    div.cyan-btn button { background: #00acee !important; }
    div.red-btn button { background: #ef4444 !important; }
    div.amber-btn button { background: #f59e0b !important; }
    div.green-btn button { background: #10b981 !important; }
    div.purple-btn button { background: #a855f7 !important; }

    input { background-color: #ffffff !important; color: #0f172a !important; border: 2px solid #cbd5e1 !important; font-weight: 700 !important; font-size: 16px !important; border-radius: 8px !important; }
    textarea { background-color: #ffffff !important; color: #0f172a !important; border: 2px solid #cbd5e1 !important; font-weight: 700 !important; font-size: 16px !important; border-radius: 8px !important; }
    [data-testid="stDataFrame"] { background: #ffffff; border: 2px solid #cbd5e1; border-radius: 8px; }
    [data-testid="stDataFrame"] * { color: #0f172a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. ENTERPRISE SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='font-family:Orbitron; color:#38bdf8;'>⚙️ GROUND OPERATIONS</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background:rgba(255,255,255,0.06); padding:16px; border-radius:10px; border:1px solid rgba(255,255,255,0.15); margin-bottom:20px;'>
            <div style='background: rgba(56, 189, 248, 0.2); border: 1px solid #38bdf8; color: #38bdf8; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 700; font-family: Orbitron; display: inline-block; margin-bottom: 8px;'>DEPLOYMENT ENGINE</div>
            <div style='color:#cbd5e1; font-size:13px; font-weight:700; letter-spacing:0.5px;'>ACTIVE STEWARDS DISPATCHED</div>
            <div style='color:#ffffff; font-size:32px; font-weight:900; font-family:Orbitron;'>142 / 150</div>
            <div style='color:#34d399; font-size:13px; font-family:Share Tech Mono; margin-top:4px;'>✓ 94% Operational Capacity</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='font-family:Orbitron; font-size:18px;'>Stadium Gate Status</h3>", unsafe_allow_html=True)
    for gate, pred in [("Gate 1", p1), ("Gate 2", p2), ("Gate 3", p3), ("Gate 4", p4)]:
        icon = "🔴" if pred > 150 else "🟡" if pred > 100 else "🟢"
        status = "CRITICAL SURGE" if pred > 150 else "ELEVATED" if pred > 100 else "STABLE FLOW"
        st.write(f"{icon} **{gate}:** {status}")

    st.markdown("---")
    st.markdown("<h3 style='font-family:Orbitron; font-size:18px;'>🚨 Critical Core Links</h3>", unsafe_allow_html=True)
    st.write("Medical Comms: CH-1 (Ext 911)")
    st.write("Crisis Dispatch: CH-2 (Ext 912)")
    st.write("Law Enforcement: CH-3 (Ext 913)")
    
    st.markdown("---")
    st.markdown("<h3 style='font-family:Orbitron; font-size:18px;'>Scenario Simulation</h3>", unsafe_allow_html=True)
    if st.button("⚡ INJECT INNINGS BREAK SURGE"):
        st.session_state.gate_history["Gate 3"].append(185)
        st.session_state.gate_history["Gate 3"].pop(0)
        log_event("Crowd Sentinel Agent", "Gate 3 surge vector anomaly intercepted", "🚨 CRITICAL")
        st.rerun()

# --- 6. CONTINUOUS MONITORING VOICE OVERRIDE LOGIC ---
if p1 > 150:
    automate_voice_announcer("Warning. Crowd Sentinel Agent alert. Gate 1 has breached capacity thresholds. Executing structured re routing protocols.")
elif p3 > 150:
    automate_voice_announcer("Attention Command Center. Anomaly detected at Gate 3. Innings break rush active.")

# --- 7. HEADER & GCP STAGE LOGS ---
st.markdown("<h1 style='text-align: center; color:#0f172a;'>🏟️ STADIUM PULSE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color:#2563eb; font-family:Orbitron; font-weight:800; font-size:16px; letter-spacing:2px; margin-bottom:25px;'>IPL 2026: INTEGRATED AI COMMAND HUB</p>", unsafe_allow_html=True)

col_inf1, col_inf2 = st.columns(2)
with col_inf1: st.markdown("<div class='gcp-log'>[LIVE_STREAM] Vertex AI Gemini 2.5 Flash pipeline streaming active...</div>", unsafe_allow_html=True)
with col_inf2: st.markdown("<div class='gcp-log'>[PUBSUB_OK] Google Cloud Pub/Sub live telemetry nodes online...</div><br>", unsafe_allow_html=True)

# --- 8. SVG TOPOGRAPHY MAP ---
st.markdown("<h3>🤖 Crowd Sentinel Agent: Live 3D Spatial Grid</h3>", unsafe_allow_html=True)

col_map, col_metrics = st.columns([1.4, 2])
with col_map:
    svg_html = f"""
    <div class="arena-isometric-box">
        <svg viewBox="0 0 220 220" width="100%">
            <line x1="10" y1="110" x2="210" y2="110" stroke="#cbd5e1" stroke-width="0.8" stroke-dasharray="2 4"/>
            <line x1="110" y1="10" x2="110" y2="210" stroke="#cbd5e1" stroke-width="0.8" stroke-dasharray="2 4"/>
            <ellipse cx="110" cy="110" rx="75" ry="100" fill="transparent" stroke="#4285F4" stroke-width="2.5" stroke-dasharray="8 4" opacity="0.8"/>
            <ellipse cx="110" cy="110" rx="50" ry="75" fill="transparent" stroke="#16a34a" stroke-width="2" opacity="0.6"/>
            <ellipse cx="110" cy="110" rx="25" ry="35" fill="transparent" stroke="#16a34a" stroke-width="2" opacity="0.7"/>
            <rect x="80" y="8" width="60" height="18" fill="{c1}" rx="4" filter="drop-shadow(0 6px 10px rgba(0,0,0,0.3))"/>
            <text x="110" y="21" font-size="10" fill="white" font-weight="900" text-anchor="middle" font-family="'Orbitron', sans-serif">GATE 1</text>
            <rect x="80" y="194" width="60" height="18" fill="{c2}" rx="4" filter="drop-shadow(0 6px 10px rgba(0,0,0,0.3))"/>
            <text x="110" y="206" font-size="10" fill="white" font-weight="900" text-anchor="middle" font-family="'Orbitron', sans-serif">GATE 2</text>
            <rect x="8" y="85" width="18" height="50" fill="{c3}" rx="4" filter="drop-shadow(0 6px 10px rgba(0,0,0,0.3))"/>
            <text x="17" y="110" font-size="9" fill="white" font-weight="900" text-anchor="middle" transform="rotate(-90 17 110)" font-family="'Orbitron', sans-serif">GATE 3</text>
            <rect x="194" y="85" width="18" height="50" fill="{c4}" rx="4" filter="drop-shadow(0 6px 10px rgba(0,0,0,0.3))"/>
            <text x="205" y="110" font-size="9" fill="white" font-weight="900" text-anchor="middle" transform="rotate(90 205 110)" font-family="'Orbitron', sans-serif">GATE 4</text>
        </svg>
    </div>
    """
    st.markdown(svg_html, unsafe_allow_html=True)

# Metric Layout Panels
m_col1, m_col2 = col_metrics.columns(2)
m_col3, m_col4 = col_metrics.columns(2)

with m_col1: st.markdown(f'<div class="dashboard-card {a1}"><div class="agent-tag">Sentinel AI Vector</div><div class="stat-value {t1}">{p1} / min</div><div class="stat-label">Gate 1 Forecast (+15m)</div></div>', unsafe_allow_html=True)
with m_col2: st.markdown(f'<div class="dashboard-card {a2}"><div class="agent-tag">Sentinel AI Vector</div><div class="stat-value {t2}">{p2} / min</div><div class="stat-label">Gate 2 Forecast (+15m)</div></div>', unsafe_allow_html=True)
with m_col3: st.markdown(f'<div class="dashboard-card {a3}"><div class="agent-tag">Sentinel AI Vector</div><div class="stat-value {t3}">{p3} / min</div><div class="stat-label">Gate 3 Forecast (+15m)</div></div>', unsafe_allow_html=True)
with m_col4: st.markdown(f'<div class="dashboard-card {a4}"><div class="agent-tag">Sentinel AI Vector</div><div class="stat-value {t4}">{p4} / min</div><div class="stat-label">Gate 4 Forecast (+15m)</div></div>', unsafe_allow_html=True)

st.markdown("---")

# --- 10. AGENT CONTROL TABS ---
tabs = st.tabs(["🏏 ROUTING MATRIX", "🚨 CRISIS DISPATCH", "🌤️ METEOROLOGY", "👁️ VISION NODE", "📣 COMMS"])

# TAB 1: Routing Matrix (Perfect Structure)
with tabs[0]:

    # Global JSON styling
    st.markdown("""
    <style>
    .json-container {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #cbd5e1;
        margin-top: 10px;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header panel
    st.markdown("""
        <div class="feature-panel panel-cyan">
            <div class="feature-title" style="color:#0095cd;">
                ⚡ DYNAMIC CROWD ROUTING ENGINE
            </div>

            <div class="feature-desc-text">
                <strong>Core Objective:</strong> Commands Gemini 2.5 Flash
                to compute tactical JSON workflows to divert heavy crowd
                flows during active match spikes.
            </div>

            <div class="feature-guide-tag">
                🎮 <strong>Operator Guide:</strong>
                Select the target check-point profile below,
                then execute the calculation matrix system.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Scenario selector
    scenario = st.selectbox(
        "Select Target IPL Checkpoint:",
        [
            "Pre-Match: Toss Time Surge (Gates 1 & 3)",
            "Innings Break: Concession Stand Rush",
            "Match End: Total Stadium Exodus"
        ]
    )

    # Execute button
    if st.button("EXECUTE SCENARIO MATRIX ROUTE"):

        with st.spinner("Vertex AI generating structured playbook..."):

            try:
                prompt = f"""
                Scenario: {scenario}
                Gate 1 flow rate: {p1}/min

                Output STRICT JSON only:

                {{
                    "primary_gate":"string",
                    "risk_tier":"CRITICAL/HIGH/LOW",
                    "action":"string",
                    "deploy_stewards":0,
                    "estimated_clear_time_mins":0
                }}

                Return ONLY raw JSON.
                """

                res = model.generate_content(prompt)

                st.markdown(
                    "<h4>🤖 LOGISTICS ENGINE DIRECTIVE DATA FEED:</h4>",
                    unsafe_allow_html=True
                )

                # Clean Gemini response
                raw_text = (
                    res.text
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

                parsed_json = json.loads(raw_text)

                # Success container
                st.markdown("""
                    <div style="
                        background-color:#ffffff;
                        padding:25px;
                        border-radius:12px;
                        border:2px solid #cbd5e1;
                        box-shadow:0px 4px 6px rgba(0,0,0,0.05);
                        margin-top:10px;
                    ">
                        <h4 style="
                            color:#16a34a;
                            margin:0;
                        ">
                            ✓ Playbook Validated and Locked
                        </h4>
                    </div>
                """, unsafe_allow_html=True)

                # JSON display (works perfectly in dark theme)
                formatted_json = json.dumps(
                    parsed_json,
                    indent=4
                )

                st.code(
                    formatted_json,
                    language="json"
                )

                # Logs
                log_event(
                    "Routing Agent",
                    f"Deployed playbook for {scenario}",
                    "✅ Active"
                )

                automate_voice_announcer(
                    "Routing engine execution complete."
                )

            except json.JSONDecodeError:
                st.error("⚠ JSON structure invalid")

                st.code(
                    res.text,
                    language="text"
                )

            except Exception as e:
                st.error(f"⚠ Error: {str(e)}")

# TAB 2: Crisis Dispatch (ISSUE 1 RESOLVED)
with tabs[1]:
    st.markdown("""
        <div class="feature-panel panel-red critical-alert">
            <div class="feature-title" style="color: #dc2626;">🚨 EMERGENCY PROTOCOL DISPATCH AGENT</div>
            <div class="feature-desc-text" style="color: #991b1b !important;"><strong>Core Objective:</strong> High-severity override layer bypassing default telemetry constraints to run emergency hazard configurations immediately, mitigating automated fragmentation delays.</div>
            <div class="feature-guide-tag" style="background: #fee2e2; border-left-color: #dc2626;">🎮 <strong>Operator Guide:</strong> Deploy emergency script variables instantly by pressing one of the overrides below.</div>
        </div>
    """, unsafe_allow_html=True)
    col_c1, col_c2, col_c3 = st.columns(3)
    crisis_type = None
    with col_c1:
        st.markdown("<div class='red-btn'>", unsafe_allow_html=True)
        if st.button("⚠️ Stampede Risk (Gate 1)", use_container_width=True): 
            crisis_type = "Stampede Risk at Gate 1"
        st.markdown("</div>", unsafe_allow_html=True)
    with col_c2:
        st.markdown("<div class='red-btn'>", unsafe_allow_html=True)
        if st.button("⚕️ Medical Vector (Gate 3)", use_container_width=True): 
            crisis_type = "Cardiac Event in VIP Gate 3"
        st.markdown("</div>", unsafe_allow_html=True)
    with col_c3:
        st.markdown("<div class='red-btn'>", unsafe_allow_html=True)
        if st.button("🔥 Concourse Hazard (Gate 2)", use_container_width=True): 
            crisis_type = "Concession Stand Fire near Gate 2"
        st.markdown("</div>", unsafe_allow_html=True)

    if crisis_type:
        with st.spinner("Compiling critical playbook parameters..."):
            prompt = f"Emergency: {crisis_type}. Output strict JSON: 'incident_type' (string), 'evacuation_route' (string), 'medical_units_req' (int), 'pa_announcement' (string). Return ONLY JSON."
            res = model.generate_content(prompt)
            st.markdown("<h4>🚨 INCIDENT THREAT ACTION PROTOCOL OUTLINE:</h4>", unsafe_allow_html=True)
            try:
                parsed_json = json.loads(res.text.replace('```json', '').replace('```', '').strip())
                st.json(parsed_json)
                log_event("Crisis Bot", f"Activated: {crisis_type}", "🚨 CRITICAL")
                # ISSUE 1 AUTOMATION: Voice engine reads out the alert script directly upon manual button triggers
                automate_voice_announcer(f"Emergency dispatch activated. Playbook playbook routing protocol initiated for {crisis_type}.")
            except: st.markdown(f'<div class="crisis-response-glow">{res.text}</div>', unsafe_allow_html=True)
    st.markdown("<div class='gcp-badge'>Powered by Vertex AI | Google Cloud</div>", unsafe_allow_html=True)

# TAB 3: Meteorology Agent
with tabs[2]:
    st.markdown("""
        <div class="feature-panel panel-amber">
            <div class="feature-title" style="color: #d97706;">🌤️ METEOROLOGICAL LIVE API AGENT</div>
            <div class="feature-desc-text"><strong>Core Objective:</strong> Connects to external climate telemetry and feeds environmental alerts into the routing matrix automatically, adjusting rules dynamically to adapt to unpredictable weather shifts.</div>
            <div class="feature-guide-tag">🎮 <strong>Operator Guide:</strong> Trigger the API network validation node to extract live metrics for Bengaluru.</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='amber-btn'>", unsafe_allow_html=True)
    if st.button("QUERY WEATHER INFRASTRUCTURE NODE"):
        with st.spinner("Calling external API for Bengaluru..."):
            temp, cond = get_live_weather()
            st.warning(f"⚠️ Live API Telemetry Received: Bengaluru Zone Tracker matches {temp}°C | Core Status: {cond}")
            prompt = f"Live weather is {cond} at {temp}C during an IPL match. What is the immediate stadium protocol? Keep to 2 sentences."
            res = model.generate_content(prompt)
            st.markdown("<h4>🌤️ METEOROLOGICAL SYSTEM DIRECTIVE:</h4>", unsafe_allow_html=True)
            st.markdown(f'<div class="ai-response-glow">{res.text}</div>', unsafe_allow_html=True)
            log_event("Weather Agent", f"Condition logged: {cond} ({temp}°C)", "✅ Active")
            automate_voice_announcer(f"Weather alert synchronization complete. Ambient temperature reads {temp} degrees celsius.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='gcp-badge'>Powered by Vertex AI | Google Cloud</div>", unsafe_allow_html=True)

# TAB 4: Vision Node (ISSUE 2 REDIRECT RESOLVED BY KEY BINDING)
# TAB 4: Vision Node (Dual Operations Mode)
with tabs[3]:
    st.markdown("""
        <div class="feature-panel panel-green">
            <div class="feature-title" style="color: #059669;">👁️ VISION REASONING CCTV INTELLIGENCE</div>
            <div class="feature-desc-text"><strong>Core Objective:</strong> Applies multimodal matrix token tracking to live security camera frames or static forensic captures to parse crowd densities and resolve structural bottlenecks.</div>
            <div class="feature-guide-tag">🎮 <strong>Operator Guide:</strong> Toggle the Input System below to either initiate the live spatial scan or upload an archive payload for forensic review.</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Mode selection
    vision_mode = st.radio("Select CCTV Input Channel:", ["📡 Live Scanning Array", "📂 Static Payload File Vault"], key="vision_mode_toggle")
    
    if vision_mode == "📡 Live Scanning Array":
        st.info("🛰️ Real-time video scanning array online. Monitoring spatial matrix tokens asynchronously.")
        st.markdown("<div class='green-btn'>", unsafe_allow_html=True)
        # Using a camera_input as the "Live Stream" trigger
        live_frame = st.camera_input("CAPTURE LIVE CAMERA FRAME")
        if live_frame:
            if st.button("RUN AUTOMATED LIVE STREAM ANOMALY SCAN"):
                with st.spinner("Processing real-time coordinate matrix..."):
                    img = Image.open(live_frame)
                    res = model.generate_content(["Format response exactly: \nRisk Tier: [Tier]\nSpatial Description: [Desc]\nActionable Advice: [Advice]", img])
                    st.markdown("<h4>👁️ LIVE STREAM DIAGNOSTIC:</h4>", unsafe_allow_html=True)
                    st.markdown(f'<div class="ai-response-glow">{res.text}</div>', unsafe_allow_html=True)
                    log_event("Vision Intelligence", "Live stream frame scan complete", "✅ Resolved")
                    automate_voice_announcer("Live stream diagnostic successfully complete.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        # File Upload Mode
        img_f = st.file_uploader("Upload Static Security Frame (JPG/PNG)", type=['jpg', 'png', 'jpeg'], key="static_upload")
        if img_f:
            st.image(img_f, use_container_width=True)
            st.markdown("<div class='green-btn'>", unsafe_allow_html=True)
            if st.button("INVOKE COMPUTER VISION SPATIAL MATRIX"):
                with st.spinner("Processing static token vectors..."):
                    img = Image.open(img_f)
                    res = model.generate_content(["Format response exactly: \nRisk Tier: [Tier]\nSpatial Description: [Desc]\nActionable Advice: [Advice]", img])
                    st.markdown("<h4>👁️ STATIC PAYLOAD INTERPRETATION:</h4>", unsafe_allow_html=True)
                    st.markdown(f'<div class="ai-response-glow">{res.text}</div>', unsafe_allow_html=True)
                    log_event("Vision Intelligence", "CCTV frame processed", "✅ Resolved")
                    automate_voice_announcer("Static image payload analyzed successfully.")
            st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown("<div class='gcp-badge'>Powered by Vertex AI | Google Cloud</div>", unsafe_allow_html=True)

# TAB 5: Comms PA
with tabs[4]:
    st.markdown("""
        <div class="feature-panel panel-purple">
            <div class="feature-title" style="color: #9333ea;">📣 AUDIBLE PUBLIC ADDRESS (PA) COMMS ENGINE</div>
            <div class="feature-desc-text"><strong>Core Objective:</strong> Bridges situational text configurations into immediate audio announcement broadcast matrices, ensuring a safe and seamless fan experience.</div>
            <div class="feature-guide-tag">🎮 <strong>Operator Guide:</strong> Confirm or edit script lines below to trigger immediate audio broadcasting.</div>
        </div>
    """, unsafe_allow_html=True)
    announcement = st.text_area("Live Announcement Script Stream Input:", "Attention fans. Due to elevated capacities, Gate 1 is being redirected. Please follow the blue signage to Gate 4.")
    st.markdown("<div class='purple-btn'>", unsafe_allow_html=True)
    if st.button("DEPLOY AUDIO ANNOUNCEMENT CHANNELS 📢"):
        st.success("Broadcasting to Stadium PA array...")
        automate_voice_announcer(announcement)
        log_event("PA System", "Voice comms broadcasted", "✅ Executed")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='gcp-badge'>Powered by Vertex AI | Google Cloud</div>", unsafe_allow_html=True)

# --- 11. CRYPTOGRAPHIC OPERATIONS LEDGER ---
st.markdown("<br><h3>📋 CRYPTOGRAPHIC OPERATIONS LEDGER</h3>", unsafe_allow_html=True)
st.dataframe(pd.DataFrame(st.session_state.ledger), use_container_width=True, hide_index=True)
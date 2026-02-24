import sys
import os
import time
import streamlit as st
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.monitoring_agent import MonitoringAgent
from agents.risk_agent import RiskAssessmentAgent
from agents.logistics_agent import LogisticsAgent

st.set_page_config(page_title="AetherSea Control Center", layout="wide")

st.title("🌊 AetherSea Autonomous Response System")

# Persistent agents (important)
if "monitoring" not in st.session_state:
    st.session_state.monitoring = MonitoringAgent()
    st.session_state.risk_agent = RiskAssessmentAgent()
    st.session_state.logistics = LogisticsAgent()
    st.session_state.risk_history = []

monitoring = st.session_state.monitoring
risk_agent = st.session_state.risk_agent
logistics = st.session_state.logistics

# Live update loop
environment_data = monitoring.collect_environment_data()
risk_report = risk_agent.evaluate(environment_data)
logistics_report = logistics.decide_action(risk_report)

st.session_state.risk_history.append(risk_report["risk_score"])

# ---- TOP METRICS ----
col1, col2, col3 = st.columns(3)

col1.metric("Risk Score", risk_report["risk_score"])
col2.metric("Severity", risk_report["severity"])
col3.metric("Trend", risk_report["trend"])

# ---- ENVIRONMENT ----
st.subheader("Environmental Conditions")

col4, col5 = st.columns(2)
col4.metric("Wind Factor", environment_data["environment"]["wind_factor"])
col5.metric("Current Strength", environment_data["environment"]["current_strength"])

st.metric("Environmental Pressure", risk_report["environmental_pressure"])

# ---- LOGISTICS ----
st.subheader("Mission Decision")

st.write("Recommended Action:", logistics_report["recommended_action"])
st.write("High Risk Streak:", logistics_report["high_risk_streak"])
st.write("Acceleration Detected:", risk_report["acceleration_detected"])

# ---- RISK GRAPH ----
st.subheader("Risk Over Time")

fig, ax = plt.subplots()
ax.plot(st.session_state.risk_history)
ax.set_xlabel("Time Step")
ax.set_ylabel("Risk Score")

st.pyplot(fig)

time.sleep(2)
st.rerun()
import streamlit as st
import math

from dashboard.stratergy_engine import compare_strategies
from dashboard.visualisations import (
    risk_over_time_chart,
    peak_risk_bar_chart,
    spatial_map
)
from dashboard.spatial_simulation import simulate_spatial_drift


# ---------------------------
# Fleet Routing Logic
# ---------------------------

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)

    a = (
        math.sin(dLat/2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dLon/2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def compute_optimal_intercept(start_lat, start_lon, drift_coords, vessel_speed):
    """
    Finds earliest intercept point based on vessel speed (km/day).
    """
    best_day = None
    best_distance = None

    for day, (d_lat, d_lon) in enumerate(drift_coords):
        distance = haversine(start_lat, start_lon, d_lat, d_lon)
        travel_time = distance / vessel_speed

        if travel_time <= day:
            best_day = day
            best_distance = distance
            break

    # If no early intercept possible → intercept at final point
    if best_day is None:
        best_day = len(drift_coords) - 1
        best_distance = haversine(
            start_lat,
            start_lon,
            drift_coords[-1][0],
            drift_coords[-1][1],
        )

    intercept_point = drift_coords[best_day]

    path = [(start_lat, start_lon), intercept_point]

    return {
        "intercept_day": best_day,
        "distance": best_distance,
        "path": path
    }


# ---------------------------
# Streamlit UI
# ---------------------------

st.set_page_config(layout="wide")
st.title("🌊 AetherSea Marine Response Control Room")

st.markdown(
    "<h3 style='color:#00d4ff;'>Real-Time Environmental Strategy & Fleet Optimization</h3>",
    unsafe_allow_html=True
)

# ---------------------------
# Sidebar Inputs
# ---------------------------

st.sidebar.header("Environmental Inputs")

D0 = st.sidebar.slider("Initial Plastic Density", 10, 100, 50)
C = st.sidebar.slider("Ocean Current Strength", 1, 10, 5)
W = st.sidebar.slider("Wind Influence", 1, 10, 5)
L = st.sidebar.slider("Distance to Coast (km)", 1, 20, 10)

st.sidebar.header("Spatial Inputs")

lat = st.sidebar.number_input("Garbage Latitude", value=12.0)
lon = st.sidebar.number_input("Garbage Longitude", value=72.0)

fleet_lat = st.sidebar.number_input("Fleet Base Latitude", value=11.5)
fleet_lon = st.sidebar.number_input("Fleet Base Longitude", value=71.5)

vessel_speed = st.sidebar.slider(
    "Vessel Speed (km per day)", 50, 500, 150
)

# ---------------------------
# Strategy Simulation
# ---------------------------

results, best_strategy = compare_strategies(D0, C, W, L)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        risk_over_time_chart(results),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        peak_risk_bar_chart(results),
        use_container_width=True
    )

# ---------------------------
# AI Decision Section
# ---------------------------

st.subheader("🧠 AI Strategy Decision Engine")
st.success(f"Recommended Strategy: {best_strategy}")

data = results[best_strategy]

st.write("### Strategy Performance Summary")
st.write(f"""
• Final Risk after 7 days: **{data['final_risk']:.2f}**  
• Peak Risk observed: **{data['peak_risk']:.2f}**  
• Operational Cost Score: **{data['cost']}**  
• Utility Score: **{data['utility_score']:.2f}**
""")

# ---------------------------
# Spatial Drift Simulation
# ---------------------------

drift_coords = simulate_spatial_drift(lat, lon, C, W)

# ---------------------------
# Fleet Optimal Intercept
# ---------------------------

intercept_data = compute_optimal_intercept(
    fleet_lat,
    fleet_lon,
    drift_coords,
    vessel_speed
)

intercept_day = intercept_data["intercept_day"]
distance = intercept_data["distance"]
path_coords = intercept_data["path"]

# ---------------------------
# Map Section
# ---------------------------

st.divider()
st.subheader("🌍 Marine Drift & Optimal Fleet Interception")

st.plotly_chart(
    spatial_map(drift_coords, path_coords),
    use_container_width=True
)

st.write("### 🚢 Fleet Interception Analysis")

st.write(f"""
• Optimal Intercept Day: **Day {intercept_day}**  
• Travel Distance: **{distance:.2f} km**  
• Vessel Speed: **{vessel_speed} km/day**  
• Estimated Travel Time: **{distance / vessel_speed:.2f} days**
""")

# ---------------------------
# Combined Strategic Explanation
# ---------------------------

st.subheader("📊 Integrated Operational Justification")

st.write(f"""
The AI recommends **{best_strategy}** based on a 7-day
risk–cost utility optimization model.

Simultaneously, fleet routing optimization determines
that interception is feasible on **Day {intercept_day}**,
minimizing spread escalation before coastal impact.

This integrated decision framework ensures:

• Environmental risk reduction  
• Cost-aware intervention  
• Minimum intercept delay  
• Operational efficiency  
""")
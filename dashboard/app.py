import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

from models.drift_simulation import run_simulation
from agents.cleanup_agent import CleanupAgent
from agents.route_optimizer import RouteOptimizer

st.set_page_config(layout="wide")

st.title("🌊 AETHERSEA — Ocean Plastic Cleanup AI System")

st.markdown(
"""
This system simulates **ocean plastic drift**, detects **high concentration plastic hotspots**,  
and calculates the **most efficient cleanup route for autonomous vessels**.
"""
)

st.sidebar.header("Simulation Controls")

top_hotspots = st.sidebar.slider(
    "Number of hotspots to detect",
    3,
    10,
    5
)

run_system = st.sidebar.button("Run Simulation")


def compute_route_distance(route):

    dist = 0

    for i in range(len(route)-1):

        lat1, lon1 = route[i]
        lat2, lon2 = route[i+1]

        d = np.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)

        dist += d

    return dist


if run_system:

    accumulation, latitudes, longitudes = run_simulation()

    st.header("1️⃣ Plastic Drift Simulation")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        fig1, ax1 = plt.subplots(figsize=(4,3))

        ax1.imshow(
            accumulation,
            origin="lower",
            cmap="viridis"
        )

        ax1.set_title("Plastic Accumulation Heatmap")

        st.pyplot(fig1)

    st.markdown(
    """
**What this shows**

Ocean currents move floating plastic over time.  
This simulation predicts where plastic debris will accumulate.

**Key Insight**

Brighter regions indicate **high plastic concentration zones** where cleanup efforts should focus.
"""
    )

    st.divider()

    st.header("2️⃣ Plastic Hotspot Detection")

    cleanup_agent = CleanupAgent()

    hotspots = cleanup_agent.detect_hotspots(
        accumulation,
        latitudes,
        longitudes,
        top_hotspots
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        fig2, ax2 = plt.subplots(figsize=(4,3))

        ax2.imshow(
            accumulation,
            origin="lower",
            cmap="magma"
        )

        for h in hotspots:

            lat_idx = np.abs(latitudes - h["lat"]).argmin()
            lon_idx = np.abs(longitudes - h["lon"]).argmin()

            ax2.scatter(
                lon_idx,
                lat_idx,
                color="cyan",
                s=120
            )

        ax2.set_title("Detected Plastic Hotspots")

        st.pyplot(fig2)

    st.markdown(
    """
**What this shows**

The Cleanup Agent scans the plastic distribution and detects **hotspots** — areas with the highest plastic density.

**Key Insight**

These hotspots represent the **priority regions for cleanup operations**.
"""
    )

    st.divider()

    st.header("3️⃣ Cleanup Route Optimization")

    route_agent = RouteOptimizer()

    start_location = (
        float(latitudes[0]),
        float(longitudes[0])
    )

    route = route_agent.compute_cleanup_route(
        start_location,
        hotspots
    )

    route_distance = compute_route_distance(route)

    col1, col2, col3 = st.columns(3)

    col1.metric("Hotspots Detected", len(hotspots))
    col2.metric("Cleanup Stops", len(route))
    col3.metric("Estimated Route Distance", f"{route_distance:.3f}")

    st.markdown(
    """
**What this shows**

The Route Optimization Agent calculates the **most efficient path** for a cleanup vessel to visit all hotspots.

**Key Insight**

Optimized routing reduces **fuel usage, travel time, and operational cost**.
"""
    )

    st.divider()

    st.header("4️⃣ Cleanup Route Map")

    hotspot_lats = [h["lat"] for h in hotspots]
    hotspot_lons = [h["lon"] for h in hotspots]

    route_lats = [r[0] for r in route]
    route_lons = [r[1] for r in route]

    fig_map = go.Figure()

    fig_map.add_trace(
        go.Scattergeo(
            lat=hotspot_lats,
            lon=hotspot_lons,
            mode="markers",
            marker=dict(size=10),
            name="Plastic Hotspots"
        )
    )

    fig_map.add_trace(
        go.Scattergeo(
            lat=route_lats,
            lon=route_lons,
            mode="lines+markers+text",
            text=[str(i+1) for i in range(len(route))],
            textposition="top center",
            name="Cleanup Route"
        )
    )

    fig_map.update_layout(
        height=500,
        geo=dict(
            projection_type="natural earth",
            showland=True
        )
    )

    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown(
    """
**What this shows**

The map displays **plastic hotspots and the optimized cleanup path**.

The numbered markers show the **order in which a cleanup vessel should visit each hotspot**.

**Key Insight**

This allows marine cleanup teams to **immediately deploy vessels along the most efficient route**.
"""
    )

    st.divider()

    st.header("📍 Cleanup Waypoints")

    route_table = pd.DataFrame(
        route,
        columns=["Latitude", "Longitude"]
    )

    route_table.index += 1
    route_table.index.name = "Stop Order"

    st.dataframe(route_table)

    st.markdown(
    """
**What this shows**

These coordinates represent the **exact cleanup locations** the vessel should visit.

**Key Insight**

Operational teams can directly use these coordinates to **deploy cleanup ships or autonomous vessels**.
"""
    )

    st.success("Simulation complete — cleanup route ready.")
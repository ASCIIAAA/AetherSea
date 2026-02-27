import plotly.graph_objects as go
import plotly.express as px


# ---------------------------
# Risk Over Time Line Chart
# ---------------------------

def risk_over_time_chart(results):
    fig = go.Figure()

    for strategy, data in results.items():
        fig.add_trace(go.Scatter(
            y=data["risk_over_time"],
            mode="lines+markers",
            name=strategy
        ))

    fig.update_layout(
        title="7-Day Risk Projection",
        template="plotly_dark",
        xaxis_title="Day",
        yaxis_title="Risk Level",
        height=450
    )

    return fig


# ---------------------------
# Peak Risk Bar Chart
# ---------------------------

def peak_risk_bar_chart(results):
    strategies = list(results.keys())
    peak_values = [results[s]["peak_risk"] for s in strategies]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=strategies,
        y=peak_values
    ))

    fig.update_layout(
        title="Peak Risk Comparison",
        template="plotly_dark",
        xaxis_title="Strategy",
        yaxis_title="Peak Risk",
        height=400
    )

    return fig


# ---------------------------
# Spatial Map
# ---------------------------

def spatial_map(drift_coords, path_coords):
    drift_lats = [c[0] for c in drift_coords]
    drift_lons = [c[1] for c in drift_coords]

    path_lats = [c[0] for c in path_coords]
    path_lons = [c[1] for c in path_coords]

    fig = px.scatter_mapbox(
        lat=drift_lats,
        lon=drift_lons,
        zoom=5,
        height=500
    )

    fig.add_scattermapbox(
        lat=path_lats,
        lon=path_lons,
        mode="lines+markers",
        name="Interception Path"
    )

    fig.update_layout(
        mapbox_style="carto-darkmatter",
        template="plotly_dark"
    )

    return fig
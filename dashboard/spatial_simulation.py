import numpy as np

def simulate_spatial_drift(lat, lon, C, W, days=7):
    coords = [(lat, lon)]

    for d in range(1, days):
        drift_lat = lat + (C * 0.01 * d)
        drift_lon = lon + (W * 0.01 * d)
        coords.append((drift_lat, drift_lon))

    return coords
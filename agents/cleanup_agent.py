import numpy as np


class CleanupAgent:

    def detect_hotspots(self, accumulation, latitudes, longitudes, top_n=5):
        """
        Detect top plastic accumulation zones.
        """

        flat = accumulation.flatten()
        top_indices = np.argsort(flat)[-top_n:]

        hotspots = []

        for idx in top_indices:

            lat_idx, lon_idx = np.unravel_index(idx, accumulation.shape)

            lat = float(latitudes[lat_idx])
            lon = float(longitudes[lon_idx])
            particles = int(accumulation[lat_idx, lon_idx])

            hotspots.append({
                "lat": lat,
                "lon": lon,
                "plastic": particles
            })

        return hotspots
import numpy as np


class RouteOptimizer:

    def distance(self, a, b):
        return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def compute_cleanup_route(self, start, hotspots):

        route = []

        current = start
        remaining = hotspots.copy()

        while remaining:

            nearest = min(
                remaining,
                key=lambda h: self.distance(
                    current,
                    (h["lat"], h["lon"])
                )
            )

            route.append((nearest["lat"], nearest["lon"]))

            current = (nearest["lat"], nearest["lon"])

            remaining.remove(nearest)

        return [start] + route
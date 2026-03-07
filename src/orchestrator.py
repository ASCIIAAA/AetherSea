from models.drift_simulation import run_simulation
from agents.cleanup_agent import CleanupAgent
from agents.route_optimizer import RouteOptimizer


def run_system():

    accumulation, latitudes, longitudes = run_simulation()

    cleanup = CleanupAgent()
    hotspots = cleanup.detect_hotspots(
        accumulation,
        latitudes,
        longitudes
    )

    router = RouteOptimizer()

    route = router.compute_cleanup_route(
        start=(0,0),
        hotspots=hotspots
    )

    return hotspots, route
from models.drift_model import DriftModel
import random


class MonitoringAgent:
    def __init__(self):
        self.model = DriftModel()

    def collect_environment_data(self):
        base_data = self.model.run()

        # Add dynamic environmental factors
        wind_factor = random.uniform(0.5, 1.5)
        current_strength = random.uniform(0.5, 1.5)

        base_data["environment"] = {
            "wind_factor": round(wind_factor, 2),
            "current_strength": round(current_strength, 2),
        }

        return base_data
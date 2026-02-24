import random
import math


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class DriftModel:
    def __init__(
        self,
        wind=(0.5, 0.2),
        current=(0.3, 0.4),
        hours=24,
        num_particles=30,
        port_location=(0, 0),
    ):
        self.wind = wind
        self.current = current
        self.hours = hours
        self.num_particles = num_particles
        self.port_location = port_location

    # -----------------------------
    # Core Simulation
    # -----------------------------
    def run_simulation(self):
        all_x = []
        all_y = []

        for _ in range(self.num_particles):
            start_x = random.uniform(-1, 1)
            start_y = random.uniform(-1, 1)

            particle = Particle(start_x, start_y)

            x_positions = []
            y_positions = []

            for _ in range(self.hours):
                wind_x = self.wind[0] + random.uniform(-0.1, 0.1)
                wind_y = self.wind[1] + random.uniform(-0.1, 0.1)

                rotation_strength = 0.15
                rotation_x = -rotation_strength * particle.y
                rotation_y = rotation_strength * particle.x

                total_x = wind_x + self.current[0] + rotation_x
                total_y = wind_y + self.current[1] + rotation_y

                particle.move(total_x, total_y)

                x_positions.append(particle.x)
                y_positions.append(particle.y)

            all_x.append(x_positions)
            all_y.append(y_positions)

        return all_x, all_y

    # -----------------------------
    # Spread Calculation
    # -----------------------------
    def calculate_spread(self, all_x, all_y):
        final_x = [x[-1] for x in all_x]
        final_y = [y[-1] for y in all_y]

        center_x = sum(final_x) / len(final_x)
        center_y = sum(final_y) / len(final_y)

        distances = [
            math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            for x, y in zip(final_x, final_y)
        ]

        average_spread = sum(distances) / len(distances)

        return average_spread, (center_x, center_y)

    # -----------------------------
    # Patch Movement Prediction
    # -----------------------------
    def predict_patch_movement(self, all_x, all_y):
        hours = len(all_x[0])
        center_x = []
        center_y = []

        for t in range(hours):
            x_t = [x[t] for x in all_x]
            y_t = [y[t] for y in all_y]

            center_x.append(sum(x_t) / len(x_t))
            center_y.append(sum(y_t) / len(y_t))

        vx = center_x[-1] - center_x[-2]
        vy = center_y[-1] - center_y[-2]

        future_x = []
        future_y = []

        last_x = center_x[-1]
        last_y = center_y[-1]

        for _ in range(10):
            last_x += vx
            last_y += vy
            future_x.append(last_x)
            future_y.append(last_y)

        return center_x, center_y, future_x, future_y

    # -----------------------------
    # Cleanup Route Planning
    # -----------------------------
    def plan_cleanup_route(self, future_x, future_y):
        target_x = future_x[4]
        target_y = future_y[4]

        port_x, port_y = self.port_location

        return {
            "port": (port_x, port_y),
            "target": (target_x, target_y),
        }

    # -----------------------------
    # Master Execution Method
    # -----------------------------
    def run(self):
        all_x, all_y = self.run_simulation()

        spread, center = self.calculate_spread(all_x, all_y)

        center_x, center_y, future_x, future_y = self.predict_patch_movement(
            all_x, all_y
        )

        route = self.plan_cleanup_route(future_x, future_y)

        return {
            "positions": {
                "all_x": all_x,
                "all_y": all_y,
            },
            "spread": spread,
            "current_center": center,
            "movement": {
                "center_x": center_x,
                "center_y": center_y,
                "future_x": future_x,
                "future_y": future_y,
            },
            "cleanup_route": route,
        }
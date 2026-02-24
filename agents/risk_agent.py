import math


class RiskAssessmentAgent:
    def __init__(self):
        self.previous_risk = None
        self.previous_speed = None

    def evaluate(self, environment_data):
        spread = environment_data["spread"]
        route = environment_data["cleanup_route"]
        center_x = environment_data["movement"]["center_x"]
        center_y = environment_data["movement"]["center_y"]

        wind = environment_data["environment"]["wind_factor"]
        current = environment_data["environment"]["current_strength"]

        port_x, port_y = route["port"]
        target_x, target_y = route["target"]

        distance = math.sqrt((target_x - port_x) ** 2 + (target_y - port_y) ** 2)

        # Safer movement calculation
        if len(center_x) >= 3:
            vx = center_x[-1] - center_x[-3]
            vy = center_y[-1] - center_y[-3]
        else:
            vx = 0
            vy = 0

        movement_speed = math.sqrt(vx ** 2 + vy ** 2)

        # Base severity
        if spread < 1:
            severity = "High"
        elif spread < 3:
            severity = "Moderate"
        else:
            severity = "Low"

        # Dynamic weighted risk
        environmental_pressure = (wind + current) / 2

        risk_score = (
            (4 - spread) * 2 +
            distance * 0.1 +
            movement_speed * 2
        ) * environmental_pressure

        # Detect acceleration (new dynamic behavior)
        acceleration_flag = False
        if self.previous_speed is not None:
            if movement_speed > self.previous_speed * 1.3:
                acceleration_flag = True
                risk_score *= 1.2  # amplify risk

        self.previous_speed = movement_speed

        # Trend logic
        trend = "Stable"
        if self.previous_risk is not None:
            if risk_score > self.previous_risk:
                trend = "Worsening"
                risk_score *= 1.1
            elif risk_score < self.previous_risk:
                trend = "Improving"

        self.previous_risk = risk_score

        return {
            "severity": severity,
            "risk_score": round(risk_score, 2),
            "trend": trend,
            "movement_speed": round(movement_speed, 2),
            "distance_from_port": round(distance, 2),
            "acceleration_detected": acceleration_flag,
            "environmental_pressure": round(environmental_pressure, 2),
        }
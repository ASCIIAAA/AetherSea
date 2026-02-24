class LogisticsAgent:
    def __init__(self):
        self.high_risk_counter = 0

    def decide_action(self, risk_report):
        risk_score = risk_report["risk_score"]

        if risk_score > 10:
            self.high_risk_counter += 1
        else:
            self.high_risk_counter = 0

        if self.high_risk_counter >= 3:
            action = "Full Emergency Response"
        elif risk_score > 8:
            action = "Immediate Deployment"
        elif risk_score > 4:
            action = "Prepare Vessel"
        else:
            action = "Monitor Situation"

        return {
            "recommended_action": action,
            "high_risk_streak": self.high_risk_counter
        }
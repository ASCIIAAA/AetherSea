import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.monitoring_agent import MonitoringAgent
from agents.risk_agent import RiskAssessmentAgent
from agents.logistics_agent import LogisticsAgent


def main():
    monitoring = MonitoringAgent()
    risk_agent = RiskAssessmentAgent()
    logistics = LogisticsAgent()

    print("\n=== AetherSea Live System Running ===")

    while True:
        environment_data = monitoring.collect_environment_data()
        risk_report = risk_agent.evaluate(environment_data)
        logistics_report = logistics.decide_action(risk_report)

        os.system("clear")  # Mac/Linux (use 'cls' for Windows)

        print("=== AetherSea Multi-Agent Decision Engine ===\n")

        print("Spread:", round(environment_data["spread"], 2))
        print("Wind Factor:", environment_data["environment"]["wind_factor"])
        print("Current Strength:", environment_data["environment"]["current_strength"])
        print("Environmental Pressure:", risk_report["environmental_pressure"])

        print("\nMovement Speed:", risk_report["movement_speed"])
        print("Distance From Port:", risk_report["distance_from_port"])

        print("\nSeverity:", risk_report["severity"])
        print("Risk Score:", risk_report["risk_score"])
        print("Trend:", risk_report["trend"])
        print("Acceleration Detected:", risk_report["acceleration_detected"])

        print("\nRecommended Action:", logistics_report["recommended_action"])
        print("High Risk Streak:", logistics_report["high_risk_streak"])

        time.sleep(2)


if __name__ == "__main__":
    main()
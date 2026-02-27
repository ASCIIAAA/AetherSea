import numpy as np

def simulate_strategy(strategy, D0, C, W, L, days=7):
    k = (C + W) * 0.01
    density = D0
    risk_over_time = []

    cost_table = {
        "Immediate": 80,
        "Delayed": 60,
        "Partial": 40,
        "Monitor": 0
    }

    for t in range(days):

        # Strategy logic
        if strategy == "Immediate" and t == 0:
            density *= 0.6
            k *= 0.7

        if strategy == "Delayed" and t == 5:
            density *= 0.6
            k *= 0.7

        if strategy == "Partial" and t == 0:
            density *= 0.8
            k *= 0.9

        # Natural growth
        spread = density * np.exp(k * t)

        risk = spread * (1 / L) * 100
        risk = min(risk, 100)

        risk_over_time.append(risk)

    peak_risk = max(risk_over_time)
    final_risk = risk_over_time[-1]
    initial_risk = risk_over_time[0]

    risk_reduction = initial_risk - final_risk
    cost = cost_table[strategy]
    utility_score = (risk_reduction * 1.5) - (cost * 0.5)

    return {
        "risk_over_time": risk_over_time,
        "peak_risk": peak_risk,
        "final_risk": final_risk,
        "cost": cost,
        "utility_score": utility_score
    }


def compare_strategies(D0, C, W, L):
    strategies = ["Immediate", "Delayed", "Partial", "Monitor"]
    results = {}

    for s in strategies:
        results[s] = simulate_strategy(s, D0, C, W, L)

    best_strategy = max(results, key=lambda x: results[x]["utility_score"])

    return results, best_strategy
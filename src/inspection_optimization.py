import numpy as np
from scipy.optimize import differential_evolution
from scipy.integrate import quad

from weibull import weibull_hazard, weibull_reliability


def degraded_time(beta, eta, hazard_threshold):
    """
    Find the approximate time when hazard rate exceeds the threshold.
    """
    times = np.linspace(1, 2000, 5000)

    hazards = np.array([
        weibull_hazard(t, beta, eta)
        for t in times
    ])

    index = np.argmax(hazards >= hazard_threshold)

    if hazards[index] < hazard_threshold:
        return np.inf

    return times[index]


def maintenance_cost_rate(
    params,
    beta,
    eta,
    hazard_threshold,
    inspection_cost,
    preventive_cost,
    failure_cost
):
    T_i, T_r = params

    if T_i <= 0 or T_r <= 0 or T_i >= T_r:
        return 1e9

    # Time when machine enters degraded state
    t_degraded = degraded_time(
        beta,
        eta,
        hazard_threshold
    )

    # Planned inspection times
    inspection_schedule = np.arange(
        T_i,
        T_r + T_i,
        T_i
    )

    # Default: replace at T_r
    detection_time = T_r

    # If degradation is detected at an inspection,
    # perform preventive maintenance there
    for t in inspection_schedule:
        if t >= t_degraded:
            detection_time = min(t, T_r)
            break

    # Inspections that occur before maintenance/replacement
    inspection_times = np.arange(
        T_i,
        detection_time,
        T_i
    )

    # Expected inspection cost:
    # inspection occurs only if machine survives until that time
    expected_inspection_cost = sum(
        inspection_cost
        * weibull_reliability(t, beta, eta)
        for t in inspection_times
    )

    # Probability of surviving until maintenance time
    R_T = weibull_reliability(
        detection_time,
        beta,
        eta
    )

    F_T = 1 - R_T

    # Expected maintenance/failure cost
    expected_maintenance_cost = (
        preventive_cost * R_T
        + failure_cost * F_T
    )

    total_expected_cost = (
        expected_inspection_cost
        + expected_maintenance_cost
    )

    # Expected cycle length E[min(X, detection_time)]
    cycle_length, _ = quad(
        lambda t: weibull_reliability(
            t,
            beta,
            eta
        ),
        0,
        detection_time
    )

    return total_expected_cost / cycle_length
if __name__ == "__main__":

    beta = 1.9267
    eta = 474.2850

    hazard_threshold = 0.004

    inspection_cost = 20
    preventive_cost = 100
    failure_cost = 1000

    bounds = [
        (20, 200),   # T_i
        (100, 800)   # T_r
    ]

    result = differential_evolution(
        lambda x: maintenance_cost_rate(
            x,
            beta,
            eta,
            hazard_threshold,
            inspection_cost,
            preventive_cost,
            failure_cost
        ),
        bounds=bounds,
        seed=42
    )

    optimal_Ti = result.x[0]
    optimal_Tr = result.x[1]
    optimal_cost = result.fun

    print(
        f"Optimal inspection interval: "
        f"{optimal_Ti:.2f} hours"
    )

    print(
        f"Optimal replacement interval: "
        f"{optimal_Tr:.2f} hours"
    )

    print(
        f"Minimum expected cost rate: "
        f"{optimal_cost:.4f} per hour"
    )
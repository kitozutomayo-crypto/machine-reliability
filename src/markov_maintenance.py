import numpy as np
import matplotlib.pyplot as plt

from scipy.linalg import expm
from scipy.optimize import minimize_scalar

from markov_model import build_generator


def maintenance_cost_rate(
    inspection_interval,
    Q,
    inspection_cost,
    preventive_cost,
    failure_cost,
    tolerance=1e-10,
    max_steps=10000
):
    """
    Long-run expected maintenance cost per hour.

    Policy:
    - Inspect every inspection_interval hours.
    - Healthy: continue operating.
    - Degraded: continue operating.
    - Critical: preventive replacement at inspection.
    - Failed: corrective replacement.
    """

    T = inspection_interval

    # Transient states:
    # 0 = Healthy
    # 1 = Degraded
    # 2 = Critical
    S = Q[:3, :3]

    # Transition matrix among transient states
    A = expm(S * T)

    # Integral of exp(S * t) from 0 to T
    integral_matrix = np.linalg.solve(
        S,
        A - np.eye(3)
    )

    ones = np.ones(3)

    # Every maintenance cycle starts from Healthy
    state_prob = np.array([
        1.0,
        0.0,
        0.0
    ])

    expected_cost = 0.0
    expected_cycle_length = 0.0

    for _ in range(max_steps):

        active_probability = state_prob.sum()

        if active_probability < tolerance:
            break

        # Expected operating time during this inspection interval
        expected_cycle_length += (
            state_prob
            @ integral_matrix
            @ ones
        )

        # State distribution at next inspection
        next_state = state_prob @ A

        survival_probability = next_state.sum()

        # Failure probability before the next inspection
        failure_probability = (
            active_probability
            - survival_probability
        )

        # Corrective maintenance cost
        expected_cost += (
            failure_cost
            * failure_probability
        )

        # Inspection happens only if machine survives
        expected_cost += (
            inspection_cost
            * survival_probability
        )

        # Critical state -> preventive replacement
        preventive_probability = next_state[2]

        expected_cost += (
            preventive_cost
            * preventive_probability
        )

        # Healthy and Degraded machines continue
        # Critical machines are replaced
        state_prob = np.array([
            next_state[0],
            next_state[1],
            0.0
        ])

    return expected_cost / expected_cycle_length


def optimize_inspection_interval(
    Q,
    inspection_cost,
    preventive_cost,
    failure_cost
):
    """
    Find the inspection interval that minimizes
    the long-run expected maintenance cost rate.
    """

    result = minimize_scalar(
        lambda T: maintenance_cost_rate(
            T,
            Q,
            inspection_cost,
            preventive_cost,
            failure_cost
        ),
        bounds=(5, 500),
        method="bounded"
    )

    return result.x, result.fun


if __name__ == "__main__":

    # -----------------------------
    # CTMC parameters
    # -----------------------------

    lambda_01 = 0.002
    lambda_12 = 0.004
    lambda_23 = 0.008

    Q = build_generator(
        lambda_01,
        lambda_12,
        lambda_23
    )

    # -----------------------------
    # Cost parameters
    # -----------------------------

    inspection_cost = 20
    preventive_cost = 100
    failure_cost = 1000

    # -----------------------------
    # Main optimization
    # -----------------------------

    optimal_interval, minimum_cost_rate = (
        optimize_inspection_interval(
            Q,
            inspection_cost,
            preventive_cost,
            failure_cost
        )
    )

    print(
        f"Optimal inspection interval: "
        f"{optimal_interval:.2f} hours"
    )

    print(
        f"Minimum expected cost rate: "
        f"{minimum_cost_rate:.4f} per hour"
    )

    # -----------------------------
    # Cost Rate vs Inspection Interval
    # -----------------------------

    inspection_intervals = np.linspace(
        10,
        300,
        200
    )

    cost_rates = np.array([
        maintenance_cost_rate(
            T,
            Q,
            inspection_cost,
            preventive_cost,
            failure_cost
        )
        for T in inspection_intervals
    ])

    plt.figure()

    plt.plot(
        inspection_intervals,
        cost_rates,
        label="Expected cost rate"
    )

    plt.axvline(
        optimal_interval,
        linestyle="--",
        label=f"Optimal T = {optimal_interval:.1f} h"
    )

    plt.xlabel("Inspection Interval (hours)")
    plt.ylabel("Expected Cost per Hour")
    plt.title("CTMC Inspection Optimization")

    plt.savefig(
    "figures/ctmc_inspection_optimization.png",
    dpi=300,
    bbox_inches="tight"
)
    plt.show()

    

    # -----------------------------
    # Sensitivity Analysis:
    # Failure Cost
    # -----------------------------

    failure_costs = [
        300,
        500,
        1000,
        2000
    ]

    optimal_intervals_fc = []

    print(
        "\nSensitivity Analysis: "
        "Failure Cost"
    )

    for fc in failure_costs:

        optimal_interval_fc, minimum_cost_rate_fc = (
            optimize_inspection_interval(
                Q,
                inspection_cost,
                preventive_cost,
                fc
            )
        )

        optimal_intervals_fc.append(
            optimal_interval_fc
        )

        print(
            f"Failure cost = {fc:4d} | "
            f"Optimal inspection interval = "
            f"{optimal_interval_fc:7.2f} h | "
            f"Cost rate = "
            f"{minimum_cost_rate_fc:.4f}"
        )

    plt.figure()

    plt.plot(
        failure_costs,
        optimal_intervals_fc,
        marker="o"
    )

    plt.xlabel("Failure Cost")
    plt.ylabel(
        "Optimal Inspection Interval (hours)"
    )
    plt.title(
        "Sensitivity to Failure Cost"
    )

    plt.savefig(
    "figures/failure_cost_sensitivity.png",
    dpi=300,
    bbox_inches="tight"
)

    plt.show()

    # -----------------------------
    # Sensitivity Analysis:
    # Inspection Cost
    # -----------------------------

    inspection_costs = [
        5,
        10,
        20,
        50,
        100
    ]

    optimal_intervals_ic = []

    print(
        "\nSensitivity Analysis: "
        "Inspection Cost"
    )

    for ic in inspection_costs:

        optimal_interval_ic, minimum_cost_rate_ic = (
            optimize_inspection_interval(
                Q,
                ic,
                preventive_cost,
                failure_cost
            )
        )

        optimal_intervals_ic.append(
            optimal_interval_ic
        )

        print(
            f"Inspection cost = {ic:4d} | "
            f"Optimal inspection interval = "
            f"{optimal_interval_ic:7.2f} h | "
            f"Cost rate = "
            f"{minimum_cost_rate_ic:.4f}"
        )

    plt.figure()

    plt.plot(
        inspection_costs,
        optimal_intervals_ic,
        marker="o"
    )

    plt.xlabel("Inspection Cost")
    plt.ylabel(
        "Optimal Inspection Interval (hours)"
    )
    plt.title(
        "Sensitivity to Inspection Cost"
    )

    plt.savefig(
    "figures/inspection_cost_sensitivity.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
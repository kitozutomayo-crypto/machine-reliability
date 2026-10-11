import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import quad

from weibull import weibull_reliability


def expected_cycle_length(T, beta, eta):
    """
    Expected length of one replacement cycle.
    E[min(X, T)] = integral_0^T R(t) dt
    """
    result, _ = quad(
        lambda t: weibull_reliability(t, beta, eta),
        0,
        T
    )

    return result


def cost_rate(T, beta, eta, preventive_cost, failure_cost):
    """
    Long-run expected maintenance cost per hour.
    """
    R_T = weibull_reliability(T, beta, eta)
    F_T = 1 - R_T

    expected_cost = (
        preventive_cost * R_T
        + failure_cost * F_T
    )

    cycle_length = expected_cycle_length(
        T,
        beta,
        eta
    )

    return expected_cost / cycle_length


if __name__ == "__main__":

    beta = 1.9267
    eta = 474.2850

    preventive_cost = 100
    failure_cost = 1000

    maintenance_times = np.linspace(20, 800, 300)

    cost_rates = np.array([
        cost_rate(
            T,
            beta,
            eta,
            preventive_cost,
            failure_cost
        )
        for T in maintenance_times
    ])

    optimal_index = np.argmin(cost_rates)

    optimal_time = maintenance_times[optimal_index]
    optimal_cost_rate = cost_rates[optimal_index]

    print(f"Optimal maintenance time: {optimal_time:.2f} hours")
    print(
        f"Minimum expected cost rate: "
        f"{optimal_cost_rate:.4f} per hour"
    )
# Sensitivity analysis

failure_costs = [300, 500, 1000, 2000]

print("\nSensitivity Analysis")

for failure_cost in failure_costs:

    cost_rates = np.array([
        cost_rate(
            T,
            beta,
            eta,
            preventive_cost,
            failure_cost
        )
        for T in maintenance_times
    ])

    optimal_index = np.argmin(cost_rates)

    optimal_time = maintenance_times[optimal_index]
    optimal_cost_rate = cost_rates[optimal_index]

    print(
        f"Failure cost = {failure_cost:4d} | "
        f"Optimal T = {optimal_time:7.2f} h | "
        f"Cost rate = {optimal_cost_rate:.4f}"
    )
    plt.plot(
        maintenance_times,
        cost_rates,
        label="Expected cost rate"
    )

    plt.axvline(
        optimal_time,
        linestyle="--",
        label=f"Optimal T = {optimal_time:.1f} h"
    )

    plt.xlabel("Preventive Maintenance Time (hours)")
    plt.ylabel("Expected Cost per Hour")
    plt.title("Maintenance Cost Optimization")

    plt.legend()
    plt.grid(True)

    plt.show()
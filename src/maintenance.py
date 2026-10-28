import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import quad
from scipy.optimize import minimize_scalar

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


def optimize_maintenance(
    beta,
    eta,
    preventive_cost,
    failure_cost
):
    result = minimize_scalar(
        lambda T: cost_rate(
            T,
            beta,
            eta,
            preventive_cost,
            failure_cost
        ),
        bounds=(20, 800),
        method="bounded"
    )

    return result.x, result.fun


if __name__ == "__main__":

    beta = 1.9267
    eta = 474.2850

    preventive_cost = 100
    failure_cost = 1000

    optimal_time, optimal_cost_rate = optimize_maintenance(
        beta,
        eta,
        preventive_cost,
        failure_cost
    )

    print(f"Optimal maintenance time: {optimal_time:.2f} hours")
    print(
        f"Minimum expected cost rate: "
        f"{optimal_cost_rate:.4f} per hour"
    )

    # Sensitivity analysis

    failure_costs = [300, 500, 1000, 2000]
    maintenance_times = np.linspace(20, 800, 300)

    print("\nSensitivity Analysis")

    for failure_cost in failure_costs:

        optimal_time, optimal_cost_rate = optimize_maintenance(
            beta,
            eta,
            preventive_cost,
            failure_cost
        )

        print(
            f"Failure cost = {failure_cost:4d} | "
            f"Optimal T = {optimal_time:7.2f} h | "
            f"Cost rate = {optimal_cost_rate:.4f}"
        )

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

        plt.plot(
            maintenance_times,
            cost_rates,
            label=f"Failure cost = {failure_cost}"
        )

    plt.xlabel("Preventive Maintenance Time (hours)")
    plt.ylabel("Expected Cost per Hour")
    plt.title("Maintenance Cost Optimization")

    plt.savefig(
    "figures/maintenance_cost_optimization.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()



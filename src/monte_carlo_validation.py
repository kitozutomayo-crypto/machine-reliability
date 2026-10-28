import numpy as np

from markov_model import build_generator
from markov_maintenance import maintenance_cost_rate
from markov_model import build_generator

def simulate_one_cycle(
    inspection_interval,
    lambda_01,
    lambda_12,
    lambda_23,
    inspection_cost,
    preventive_cost,
    failure_cost,
    rng
):
    """
    Simulate one maintenance cycle.

    States:
    0 = Healthy
    1 = Degraded
    2 = Critical
    3 = Failed
    """

    state = 0
    time = 0.0
    total_cost = 0.0

    next_inspection = inspection_interval

    while True:

        # Transition rate depends on current state
        if state == 0:
            rate = lambda_01
            next_state = 1

        elif state == 1:
            rate = lambda_12
            next_state = 2

        elif state == 2:
            rate = lambda_23
            next_state = 3

        else:
            break

        # Random waiting time until next state transition
        transition_time = rng.exponential(1 / rate)

        # Will inspection happen before next transition?
        if time + transition_time >= next_inspection:

            time = next_inspection
            total_cost += inspection_cost

            # Critical detected -> preventive replacement
            if state == 2:
                total_cost += preventive_cost
                break

            next_inspection += inspection_interval

        else:

            time += transition_time
            state = next_state

            # Failure -> corrective replacement
            if state == 3:
                total_cost += failure_cost
                break

    return time, total_cost


def monte_carlo_cost_rate(
    n_cycles,
    inspection_interval,
    lambda_01,
    lambda_12,
    lambda_23,
    inspection_cost,
    preventive_cost,
    failure_cost,
    seed=42
):
    rng = np.random.default_rng(seed)

    total_time = 0.0
    total_cost = 0.0

    for _ in range(n_cycles):

        cycle_time, cycle_cost = simulate_one_cycle(
            inspection_interval,
            lambda_01,
            lambda_12,
            lambda_23,
            inspection_cost,
            preventive_cost,
            failure_cost,
            rng
        )

        total_time += cycle_time
        total_cost += cycle_cost

    return total_cost / total_time


if __name__ == "__main__":

    lambda_01 = 0.002
    lambda_12 = 0.004
    lambda_23 = 0.008

    inspection_cost = 20
    preventive_cost = 100
    failure_cost = 1000

    Q = build_generator(
        lambda_01,
        lambda_12,
        lambda_23
    )

    intervals = [
    50,
    85.64,
    150,
    250
]
    n_cycles = 100000

theoretical_costs = []
simulated_costs = []

print("\nPolicy Comparison")

for T in intervals:

    theoretical_cost = maintenance_cost_rate(
        T,
        Q,
        inspection_cost,
        preventive_cost,
        failure_cost
    )

    simulated_cost = monte_carlo_cost_rate(
        n_cycles,
        T,
        lambda_01,
        lambda_12,
        lambda_23,
        inspection_cost,
        preventive_cost,
        failure_cost
    )

    theoretical_costs.append(
        theoretical_cost
    )

    simulated_costs.append(
        simulated_cost
    )

    print(
        f"T = {T:6.2f} h | "
        f"Theoretical = {theoretical_cost:.4f} | "
        f"Monte Carlo = {simulated_cost:.4f}"
    )
    import matplotlib.pyplot as plt


plt.figure()

plt.plot(
    intervals,
    theoretical_costs,
    marker="o",
    label="Theoretical"
)

plt.plot(
    intervals,
    simulated_costs,
    marker="o",
    label="Monte Carlo"
)

plt.xlabel("Inspection Interval (hours)")
plt.ylabel("Long-run Cost Rate")
plt.title("Maintenance Policy Comparison")

plt.legend()
plt.grid(True)
plt.axvline(
    85.64,
    linestyle="--",
    label="Optimal interval = 85.64 h"
)
plt.savefig(
    "figures/policy_comparison.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

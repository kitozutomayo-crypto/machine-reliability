from markov_model import build_generator
from markov_maintenance import optimize_inspection_interval


def run_ctmc_optimization(
    lambda_01,
    lambda_12,
    lambda_23,
    inspection_cost,
    preventive_cost,
    failure_cost
):
    Q = build_generator(
        lambda_01,
        lambda_12,
        lambda_23
    )

    optimal_interval, cost_rate = (
        optimize_inspection_interval(
            Q,
            inspection_cost,
            preventive_cost,
            failure_cost
        )
    )

    return {
        "optimal_interval": optimal_interval,
        "cost_rate": cost_rate
    }
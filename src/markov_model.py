import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm


def build_generator(lambda_01, lambda_12, lambda_23):
    """
    Build CTMC generator matrix Q.

    States:
    0 = Healthy
    1 = Degraded
    2 = Critical
    3 = Failed
    """
    Q = np.array([
        [-lambda_01,  lambda_01,      0.0,       0.0],
        [0.0,        -lambda_12,  lambda_12,      0.0],
        [0.0,          0.0,      -lambda_23, lambda_23],
        [0.0,          0.0,        0.0,       0.0]
    ])

    return Q


def transition_matrix(Q, t):
    """
    Compute P(t) = exp(Q * t)
    """
    return expm(Q * t)


if __name__ == "__main__":

    lambda_01 = 0.002
    lambda_12 = 0.004
    lambda_23 = 0.008

    Q = build_generator(
        lambda_01,
        lambda_12,
        lambda_23
    )

    print("Generator matrix Q:")
    print(Q)

    # Time range
    times = np.linspace(0, 1000, 300)

    # Initial state:
    # machine starts in Healthy state
    initial_state = np.array([
        1.0,
        0.0,
        0.0,
        0.0
    ])

    probabilities = []

    for t in times:

        P = transition_matrix(Q, t)

        state_prob = initial_state @ P

        probabilities.append(state_prob)

    probabilities = np.array(probabilities)

    # Plot state probabilities
    plt.plot(
        times,
        probabilities[:, 0],
        label="Healthy"
    )

    plt.plot(
        times,
        probabilities[:, 1],
        label="Degraded"
    )

    plt.plot(
        times,
        probabilities[:, 2],
        label="Critical"
    )

    plt.plot(
        times,
        probabilities[:, 3],
        label="Failed"
    )

    plt.xlabel("Time (hours)")
    plt.ylabel("State Probability")
    plt.title("CTMC Machine State Probabilities")

    plt.savefig(
    "figures/markov_state_probabilities.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

 
import numpy as np
import matplotlib.pyplot as plt


def weibull_reliability(t, beta, eta):
    return np.exp(-(t / eta) ** beta)


def weibull_failure_probability(t, beta, eta):
    return 1 - weibull_reliability(t, beta, eta)


def weibull_pdf(t, beta, eta):
    return (
        (beta / eta)
        * (t / eta) ** (beta - 1)
        * np.exp(-(t / eta) ** beta)
    )


def weibull_hazard(t, beta, eta):
    return (beta / eta) * (t / eta) ** (beta - 1)


if __name__ == "__main__":
    eta = 500
    time = np.linspace(1, 1500, 300)
    beta_values = [0.5, 1.0, 2.0]

    # Reliability curves
    for beta in beta_values:
        R = weibull_reliability(time, beta, eta)
        plt.plot(time, R, label=f"beta = {beta}")
def time_at_reliability(reliability, beta, eta):
    """
    Calculate the time at which reliability
    reaches a specified level.
    """
    return eta * (-np.log(reliability)) ** (1 / beta) 
    plt.xlabel("Time (hours)")
    plt.ylabel("Reliability R(t)")
    plt.title("Weibull Reliability")
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)
    plt.show()

    # Hazard curves
    for beta in beta_values:
        h = weibull_hazard(time, beta, eta)
        plt.plot(time, h, label=f"beta = {beta}")

    plt.xlabel("Time (hours)")
    plt.ylabel("Hazard Rate h(t)")
    plt.title("Weibull Hazard Rate")
    plt.legend()
    plt.grid(True)
    plt.show()
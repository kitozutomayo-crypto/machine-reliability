import numpy as np
import matplotlib.pyplot as plt


def exponential_reliability(t, failure_rate):
    """Reliability function R(t)."""
    return np.exp(-failure_rate * t)


def exponential_failure_probability(t, failure_rate):
    """Cumulative failure probability F(t)."""
    return 1 - exponential_reliability(t, failure_rate)


def exponential_pdf(t, failure_rate):
    """Failure time probability density f(t)."""
    return failure_rate * np.exp(-failure_rate * t)


def exponential_hazard(t, failure_rate):
    """Hazard rate h(t)."""
    return np.full_like(t, failure_rate, dtype=float)


if __name__ == "__main__":
    failure_rate = 0.002

    time = np.linspace(0, 2000, 200)

    R = exponential_reliability(time, failure_rate)
    F = exponential_failure_probability(time, failure_rate)
    f = exponential_pdf(time, failure_rate)
    h = exponential_hazard(time, failure_rate)

    print(f"MTTF = {1 / failure_rate:.2f} hours")

    plt.plot(time, R, label="Reliability R(t)")
    plt.plot(time, F, label="Failure probability F(t)")

    plt.xlabel("Time (hours)")
    plt.ylabel("Probability")
    plt.title("Reliability and Failure Probability")
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)

    plt.show()
    # Plot PDF
plt.plot(time, f)

plt.xlabel("Time (hours)")
plt.ylabel("Density f(t)")
plt.title("Failure Time Density")
plt.grid(True)

plt.show()


# Plot hazard rate
plt.plot(time, h)

plt.xlabel("Time (hours)")
plt.ylabel("Hazard Rate h(t)")
plt.title("Hazard Rate")
plt.grid(True)

plt.show()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import weibull_min
from scipy.special import gamma

from weibull import (
    weibull_reliability,
    time_at_reliability,
)


# Load failure data
data = pd.read_csv("data/failure_data.csv")

failure_times = data["failure_time"]


# Fit Weibull distribution using MLE
beta_hat, loc_hat, eta_hat = weibull_min.fit(
    failure_times,
    floc=0
)


# Calculate MTTF
mttf = eta_hat * gamma(1 + 1 / beta_hat)


# Print estimated parameters
print("Estimated Weibull parameters")
print(f"beta = {beta_hat:.4f}")
print(f"eta  = {eta_hat:.4f} hours")
print(f"Estimated MTTF = {mttf:.2f} hours")


# Create time points
time = np.linspace(0, 1500, 300)


# Calculate estimated reliability
estimated_R = weibull_reliability(
    time,
    beta_hat,
    eta_hat
)
reliability_targets = [0.90, 0.80, 0.50]

print("\nRecommended maintenance thresholds")

for target in reliability_targets:
    maintenance_time = time_at_reliability(
        target,
        beta_hat,
        eta_hat
    )

    print(
        f"R = {target:.0%}: "
        f"{maintenance_time:.2f} hours"
    )

# Plot estimated reliability curve
plt.plot(
    time,
    estimated_R,
    label="Estimated Weibull Reliability"
)

plt.xlabel("Time (hours)")
plt.ylabel("Reliability R(t)")
plt.title("Estimated Machine Reliability")

plt.ylim(0, 1)
plt.legend()
plt.grid(True)

plt.show()
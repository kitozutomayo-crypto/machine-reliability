import numpy as np
import pandas as pd


# Make the experiment reproducible
np.random.seed(42)

# True parameters
true_beta = 2.0
true_eta = 500

# Number of machines
n_machines = 100

# Generate Weibull failure times
failure_times = (
    true_eta
    * np.random.weibull(true_beta, n_machines)
)

# Create machine IDs
machine_ids = np.arange(1, n_machines + 1)

# Build dataset
data = pd.DataFrame({
    "machine_id": machine_ids,
    "failure_time": failure_times
})

# Save data
data.to_csv(
    "data/failure_data.csv",
    index=False
)

print(data.head())
print()
print(f"Generated {n_machines} machine failure records.")
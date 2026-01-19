import pandas as pd

# Load full dataset
df = pd.read_csv("UNSW_NB15_training-set.csv")

# Take a small random sample
small_df = df.sample(n=5000, random_state=42)

# Save small CSV
small_df.to_csv("unsw_small.csv", index=False)

print("Small CSV created:", small_df.shape)

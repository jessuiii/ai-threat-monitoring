import pandas as pd

df = pd.read_csv("unsw_small.csv")

selected_columns = [
    "rate",
    "spkts",
    "sbytes",
    "dbytes",
    "ct_src_dport_ltm",
    "ct_srv_src",
    "label"
]

df_small = df[selected_columns]

df_small.to_csv("unsw_demo.csv", index=False)

print(df_small.head())
print(df_small.shape)

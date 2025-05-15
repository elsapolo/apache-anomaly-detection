import pandas as pd
import numpy as np

from extract_raw_logs import save_to_parquet

# Step 1: Load your structured logs
# Assuming columns: path, size
df = pd.read_parquet("../ssl-logs/parquet/raw/ssl-access.log-all-url.parquet")

#TODO
'''
1. convert query dict into dict
2. '''
df["query_structure"] = df["query"]

# Step 2: Group by endpoint
grouped = df.groupby(["path", "method", "status"])

# Step 3: Compute statistics per endpoint
stats = grouped["size"].agg(["mean", "std", "count", "median"])
stats["mad"] = grouped["size"].apply(lambda x: np.median(np.abs(x - np.median(x))))

# Join stats back to the original data
df = df.merge(stats, on="path", suffixes=("", "_stats"))

# Step 4: Compute anomaly scores (z-score and MAD score)
df["z_score"] = (df["size"] - df["mean"]) / df["std"]
df["mad_score"] = np.abs(df["size"] - df["median"]) / (df["mad"] + 1e-6)

# Step 5: Flag anomalies
# Z-score > 3 or MAD score > 5 (thresholds are tunable)
df["anomalous"] = (df["z_score"].abs() > 3) | (df["mad_score"] > 5)

# Output anomalies

anomalies = df[df["anomalous"]]

print(anomalies.head())

save_to_parquet(anomalies, "../ssl-logs/parquet/size_anomalies.parquet")


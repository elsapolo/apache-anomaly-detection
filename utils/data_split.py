import pandas as pd

def split_for_analysis(df: pd.DataFrame, baseline_fraction: float = 0.8):
    """
    Splits a DataFrame into a baseline (training) and evaluation (detection) set,
    based on timestamp ordering.

    Parameters:
        df (pd.DataFrame): DataFrame containing at least a 'timestamp' column.
        baseline_fraction (float): Proportion to use for the baseline. Default is 0.8.

    Returns:
        tuple: (df_baseline, df_eval)
    """
    if "timestamp" not in df.columns:
        raise ValueError("DataFrame must contain a 'timestamp' column.")

    # Ensure timestamp is a proper datetime type
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    split_idx = int(len(df) * baseline_fraction)
    df_baseline = df.iloc[:split_idx].copy()
    df_eval = df.iloc[split_idx:].copy()

    print("📊 Data Split Summary")
    print("---------------------")
    print(f"Total entries:          {len(df):,}")
    print(f"Baseline set size:      {len(df_baseline):,}")
    print(f"Evaluation set size:    {len(df_eval):,}")
    print(f"Baseline range:         {df_baseline['timestamp'].min()} → {df_baseline['timestamp'].max()}")
    print(f"Evaluation range:       {df_eval['timestamp'].min()} → {df_eval['timestamp'].max()}")

    return df_baseline, df_eval

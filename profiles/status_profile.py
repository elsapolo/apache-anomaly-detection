import pandas as pd
from collections import defaultdict

def build_status_profile(df: pd.DataFrame, min_count: int = 20) -> dict:
    """
    Builds a baseline profile of status code distributions per (method, path).
    Filters out low-volume paths using `min_count`.

    Returns:
        dict[(method, path)] -> dict[status_code] -> float (proportion)
    """
    grouped = df.groupby(["method", "path"])["status"].value_counts(normalize=True)

    counts = df.groupby(["method", "path"]).size()
    valid = counts[counts >= min_count].index

    # Convert to nested dict structure
    profile = defaultdict(dict)
    for (method, path, status), proportion in grouped.items():
        if (method, path) in valid:
            profile[(method, path)][int(status)] = float(proportion)


    return dict(profile)

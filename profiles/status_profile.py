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

    # Convert to nested dict structure
    profile = defaultdict(dict)
    for (method, path, status), proportion in grouped.items():
        profile[(method, path)][int(status)] = float(proportion)

    # Optionally filter out method+path combos with too few entries
    counts = df.groupby(["method", "path"]).size()
    for key in list(profile.keys()):
        if counts.get(key, 0) < min_count:
            del profile[key]

    return dict(profile)

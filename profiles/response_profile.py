import pandas as pd
from collections import defaultdict

def build_response_size_profile(df: pd.DataFrame, min_count=10) -> dict:
    """
    Builds a baseline profile of response sizes grouped by
    (method, path, query_keys, status).

    Returns:
        dict[(method, path, query_keys, status)] -> {mean: float, std: float}
    """

    groups = df.groupby(["method", "path", "query_keys", "status"])
    counts = groups.size()

    profile = {}
    for group_key, count in counts.items():
        if count >= min_count:
            sizes = groups.get_group(group_key)["response_size"]
            profile[group_key] = {
                "mean": sizes.mean(),
                "std": sizes.std()
            }

    return profile

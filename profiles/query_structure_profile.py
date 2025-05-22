import pandas as pd
from collections import defaultdict

def build_query_structure_profile(df: pd.DataFrame, min_count: int = 10) -> dict:
    """
    Builds a profile of known query key sets per (method, path).
    Each (method, path) maps to a list of sorted lists of query keys.

    Parameters:
        df: DataFrame containing at least 'method', 'path', 'query_dict_str'
        min_count: minimum number of examples to keep a (method, path)

    Returns:
        dict: {
            "GET /search": [["q"], ["q", "sort"], ...],
            ...
        }
    """
    df = df.copy()
    df["query_keys"] = df["query_dict_str"].apply(lambda s: sorted(eval(s).keys()) if isinstance(s, str) and s != "null" else [])

    counts = df.groupby(["method", "path"]).size()
    valid = counts[counts >= min_count].index

    profile = defaultdict(set)
    for _, row in df.iterrows():
        key = (row["method"], row["path"])
        if key in valid:
            structure = tuple(row["query_keys"])
            profile[key].add(structure)


    return profile

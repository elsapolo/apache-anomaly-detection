import pandas as pd
from collections import defaultdict, Counter

from utils.parsing import extract_query_keys


#TODO: duplication in counts, method counting between profile builders
def build_query_structure_profile(df: pd.DataFrame, min_count: int = 10) -> dict:
    """
    Builds a frequency distribution of query structures per (method, path).
    Filters out low-volume paths using `min_count`.

    Returns:
        dict[(method,path)] -> dict[(query_param1,query_param2,...)] -> float (proportion)
    """

    counts = df.groupby(["method", "path"]).size()
    valid = counts[counts >= min_count].index

    grouped = df.groupby(["method", "path"])["query_keys"].value_counts(normalize=True)

    profile = defaultdict(dict)
    for (method, path, keys), freq in grouped.items():
        if (method, path) in valid:
            profile[(method, path)][keys] = float(freq)



    return dict(profile)

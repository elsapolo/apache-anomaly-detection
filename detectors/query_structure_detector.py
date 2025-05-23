import pandas as pd


def detect_query_structure_anomalies(df: pd.DataFrame, profile: dict, rare_threshold: float = None) -> pd.DataFrame:
    """
    Flags query structures not in the profile or below a rarity threshold.

    Adds:
        - query_structure_anomaly (bool)
        - query_structure_anomaly_reason (str)
    """

    # Count how often each structure appears in eval set
    df = df.copy()
    df["query_keys"] = df["query_dict_str"].apply(
        lambda s: tuple(sorted(eval(s).keys())) if isinstance(s, str) and s != "null" else tuple()
    )

    # Count frequencies in eval set for later rarity check
    structure_counts = df.groupby(["method", "path"])["query_keys"].value_counts(normalize=True)

    def get_reason(row):
        key = f"{row['method']} {row['path']}"
        structure = row["query_keys"]

        if key not in profile:
            return "unseen_path"

        known_structures = [tuple(sorted(keys)) for keys in profile[key]]
        if structure not in known_structures:
            return "unseen_structure"

        if rare_threshold is not None:
            freq = structure_counts.get((row["method"], row["path"], structure), 0)
            if freq < rare_threshold:
                return f"(<{rare_threshold:.2%})"

        return None

    df["query_structure_anomaly_reason"] = df.apply(get_reason, axis=1)
    df["query_structure_anomaly"] = df["query_structure_anomaly_reason"].notnull()

    return df

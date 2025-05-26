import pandas as pd

from utils.parsing import extract_query_keys


def detect_query_structure_anomalies(df: pd.DataFrame, profile: dict, rare_threshold: float = None) -> pd.DataFrame:
    """
    Flags query structures not in the profile or below a rarity threshold.

    Adds:
        - query_structure_anomaly (bool)
        - query_structure_anomaly_reason (str)
    """

    def get_reason(row):
        key = (row['method'],row['path'])
        structure = row["query_keys"]

        if key not in profile:
            return "unseen_path"

        known_structures = profile[key]

        if structure not in known_structures:
            return "unseen_structure"

        if rare_threshold is not None and known_structures[structure] < rare_threshold:
            return f"rare_structure (<{rare_threshold:.2%})"

        return None

    df["query_structure_anomaly_reason"] = df.apply(get_reason, axis=1)
    df["query_structure_anomaly"] = df["query_structure_anomaly_reason"].notnull()

    return df

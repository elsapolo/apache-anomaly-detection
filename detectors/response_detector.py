import pandas as pd

from utils.parsing import extract_query_keys_df


def detect_response_anomalies(df: pd.DataFrame, profile: dict, z_thresh: float = 2.5) -> pd.DataFrame:
    """
    Flags rows where response size deviates significantly from the baseline.

    Adds:
        - response_size_anomaly (bool)
        - response_size_anomaly_reason (str)
    """

    def get_reason_and_score(row):
        key = (row["method"], row["path"], row["query_keys"], row["status"])
        if key not in profile:
            return "unseen_group", None

        stats = profile[key]
        std = stats["std"]
        z = abs(row["response_size"] - stats["mean"]) / std if std > 0 else 0

        if z > z_thresh:
            return "size_deviation", z
        return None, None

    df[["response_size_anomaly_reason", "response_size_anomaly_score"]] = (
        df.apply(get_reason_and_score, axis=1, result_type="expand")
    )
    df["response_size_anomaly"] = df["response_size_anomaly_reason"].notnull()

    return df

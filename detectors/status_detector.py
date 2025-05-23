import pandas as pd

def detect_status_anomalies(df: pd.DataFrame, profile: dict, rare_threshold: float = None) -> pd.DataFrame:
    """
    Flags rows where (method, path, status) does not match the baseline profile.
    Adds:
        - status_anomaly (bool)
        - status_anomaly_reason (str): unseen_path | unseen_status | rare_status | None
    """

    def get_reason(row):
        key = (row['method'], row['path'])
        status = row['status']

        if key not in profile:
            return "unseen_path"

        dist = profile[key]

        if status not in dist:
            return "unseen_status"

        if rare_threshold is not None and dist[status] < rare_threshold:
            return f"rare_status (<{rare_threshold:.2%})"

        return None

    df = df.copy()
    df["status_anomaly_reason"] = df.apply(get_reason, axis=1)
    df["status_anomaly"] = df["status_anomaly_reason"].notnull()

    return df


import pandas as pd
import json

from detectors.status_detector import detect_status_anomalies
from utils.log_loading import save_parquet
from utils.log_summary import print_status_anomaly_summary


#TODO: new utils file?
def load_status_profile(path):
    with open(path) as f:
        return json.load(f)

def status_anomalies(df, profile, rare_threshold=None) -> pd.DataFrame:
    df = detect_status_anomalies(df, profile, rare_threshold)

    print_status_anomaly_summary(df)

    return df

eval_path = "../data/parsed/all_ssl-access-url-whitelisted-eval-80.parquet"
profile_path = "../data/profiles/status_profile_v1.json"
output_path = "../data/output/status_anomaly_v1.csv"

df_eval = pd.read_parquet(eval_path)
profile = load_status_profile(profile_path)

df_status_anomalies = status_anomalies(df_eval, profile, rare_threshold=0.01)

save_parquet(df_status_anomalies, output_path)



import pandas as pd
import json

from detectors.query_structure_detector import detect_query_structure_anomalies
from detectors.status_detector import detect_status_anomalies
from utils.log_loading import save_parquet
from utils.log_summary import print_status_anomaly_summary, print_query_structure_anomaly_summary
from utils.parsing import parse_query_dict_string_df
from utils.profile_loading import load_status_profile, load_query_structure_profile


def status_anomalies(df, profile_path, rare_threshold=None) -> pd.DataFrame:
    profile = load_status_profile(profile_path)

    df = detect_status_anomalies(df, profile, rare_threshold)

    print_status_anomaly_summary(df)

    return df

def query_structure_anomalies(df, profile_path, rare_threshold=None) -> pd.DataFrame:
    profile = load_query_structure_profile(profile_path)

    df = detect_query_structure_anomalies(df, profile, rare_threshold)

    print_query_structure_anomaly_summary(df)

    return df

eval_path = "../data/split/whitelisted-80-20/all_ssl-access-url-whitelisted-eval-80.parquet"
status_profile_path = "../data/profiles/status_profile_v1.json"
query_structure_profile_path = "../data/profiles/query_structure_profile_v1.json"
output_path = "../data/output/status_query_structure_anomaly_v1.parquet"


df_eval = pd.read_parquet(eval_path)
df_eval = parse_query_dict_string_df(df_eval)

df_eval= status_anomalies(df_eval, status_profile_path, rare_threshold=0.01)
df_eval = query_structure_anomalies(df_eval, query_structure_profile_path, rare_threshold=0.01)

save_parquet(df_eval, output_path)



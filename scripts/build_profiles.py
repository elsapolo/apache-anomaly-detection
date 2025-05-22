import pandas as pd
import json
from profiles.status_profile import build_status_profile
from utils.log_loading import save_parquet  # optional
from utils.data_split import split_for_analysis

def status_profile(df, output):
    print("📊 Building status profile...")
    profile = build_status_profile(df)

    serializable_profile = {
        f"{method} {path}": {str(code): prob for code, prob in dist.items()}
        for (method, path), dist in profile.items()
    }

    print(f"💾 Saving profile to {output}")
    with open(profile_output_path, "w") as f:
        json.dump(serializable_profile, f, indent=2)

input_path = "../data/parsed/all_ssl-access-url-whitelisted-train-80.parquet"
profile_output_path = "../data/profiles/status_profile_v1.json"

df_train = pd.read_parquet(input_path)
status_profile(df_train, profile_output_path)



import pandas as pd
import json

from profiles.query_structure_profile import build_query_structure_profile
from profiles.status_profile import build_status_profile

#TODO: refactor to eliminate duplication

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

def query_structure_profile(df, output):
    print("📊 Building query structure profile...")
    profile = build_query_structure_profile(df)

    # Convert to serializable form
    serializable_profile = {
        f"{method} {path}": [list(s) for s in sorted(structures)]
        for (method, path), structures in profile.items()
    }

    print(f"💾 Saving profile to {output}")
    with open(profile_output_path, "w") as f:
        json.dump(serializable_profile, f, indent=2)


input_path = "../data/split/whitelisted-80-20/all_ssl-access-url-whitelisted-train-80.parquet"
profile_output_path = "../data/profiles/status_profile_v1.json"
query_structure_output_path = "../data/profiles/query_structure_profile_v1.json"

df_train = pd.read_parquet(input_path)
#status_profile(df_train, profile_output_path) #Last built 22/05/2025 1pm
query_structure_profile(df_train, profile_output_path)


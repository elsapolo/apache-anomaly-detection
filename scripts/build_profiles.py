import pandas as pd
import json

from profiles.query_structure_profile import build_query_structure_profile
from profiles.response_profile import build_response_size_profile
from profiles.status_profile import build_status_profile
from utils.parsing import parse_query_dict_string_df, extract_query_keys_df


#TODO: refactor to eliminate duplication

def status_profile(df, output):
    print("📊 Building status profile...")
    profile = build_status_profile(df)

    serializable_profile = {
        f"{method} {path}": {str(code): prob for code, prob in dist.items()}
        for (method, path), dist in profile.items()
    }

    print(f"💾 Saving profile to {output}")
    with open(output, "w") as f:
        json.dump(serializable_profile, f, indent=2)

def query_structure_profile(df, output):
    print("📊 Building query structure profile...")
    profile = build_query_structure_profile(df)

    # Convert to serializable form
    serializable_profile = {
        f"{method} {path}": {
            json.dumps(list(query_keys)): freq
            for query_keys, freq in inner.items()
        }
        for (method, path), inner in profile.items()
    }

    print(f"💾 Saving profile to {output}")
    with open(output, "w") as f:
        json.dump(serializable_profile, f, indent=2)

def response_profile(df, output):
    print("📊 Building response profile...")
    profile = build_response_size_profile(df)

    # Convert to serializable form: stringify the 4-tuple keys
    #TODO: check this
    serializable_profile = {
        str(key): value for key, value in profile.items()
    }

    print(f"💾 Saving profile to {output}")
    with open(output, "w") as f:
        json.dump(serializable_profile, f, indent=2)


input_path = "../data/split/whitelisted-80-20/all_ssl-access-url-whitelisted-train-80.parquet"
status_profile_output_path = "../data/profiles/status_profile_v1.json"
query_structure_profile_output_path = "../data/profiles/query_structure_profile_v1.json"
response_profile_output_path = "../data/profiles/response_profile_v1.json"

df_train = pd.read_parquet(input_path)
df_train = parse_query_dict_string_df(df_train)
df_train = extract_query_keys_df(df_train)
#status_profile(df_train, status_profile_output_path) #Last built 23/05/2025 11:37
#query_structure_profile(df_train, query_structure_profile_output_path) #Last built 23/05/2025 11:37
response_profile(df_train, response_profile_output_path)
import json

import pandas as pd

from utils.log_loading import parse_apache_log_file, save_parquet
from utils.log_summary import print_request_parse_summary, print_whitelist_summary
from utils.request_parser import parse_request_line, parse_request_column
from utils.whitelisting import apply_whitelist


def parse_raw(input_path: str, output_path: str) -> pd.DataFrame:
    df = parse_apache_log_file(input_path)

    if output_path:
        df.to_parquet(output_path)

    print(f"✅ Saved {len(df)} rows to {output_path}")
    return df


def parse_request(df: pd.DataFrame, output_path = None) -> pd.DataFrame:
    df = parse_request_column(df)
    print_request_parse_summary(df)
    df["query_dict_str"] = df["query_dict"].apply(
        lambda d: json.dumps(d) if isinstance(d, dict) else None
    )

    df.drop(columns=["request", "request_error", "query_dict"], inplace=True)

    if output_path:
        save_parquet(df, output_path)

    return df

def whitelist_parsed(df: pd.DataFrame, output_path = None) -> pd.DataFrame:
    df = apply_whitelist(df)
    print_whitelist_summary(df)
    df = df[~df['whitelisted']]
    df = df.drop(columns=['whitelisted'])

    if output_path:
        save_parquet(df, output_path)

    return df


input = "../data/raw/all_ssl_access.log"
parsed_output_path = "../data/parsed/all_ssl_access.parquet"
request_parsed_output_path = "../data/parsed/all_ssl_access-url.parquet"
whitelisted_output_path = "../data/parsed/all_ssl_access-url-whitelisted.parquet"

df = pd.read_parquet(parsed_output_path)
df = parse_request(df, request_parsed_output_path)
df = whitelist_parsed(df, whitelisted_output_path)

#LAST PARSED AND WHITELISTED 22/05/2025 5pm -> after fixing broken query saving

import pandas as pd
import argparse
import os
from urllib.parse import urlparse

SAFE_EXTENSIONS = {'.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.ico', '.pdf', '.txt', '.woff2', '.svg'}
SUSPICIOUS_KEYWORDS = {'wp-login', 'admin', 'php', 'eval', 'upload', 'config', 'passwd', 'etc'}


def extract_path_and_query(request_str):
    try:
        parts = request_str.split()
        if len(parts) < 2:
            return "", ""
        url = parts[1]
        parsed = urlparse(url)
        return parsed.path.lower(), parsed.query
    except:
        return "", ""


def tag_row(row):
    path, query = extract_path_and_query(row['request'])
    ua = row.get('user_agent', '').lower()
    status = int(row['status'])

    if status >= 400:
        return 'suspicious'
    if any(keyword in path for keyword in SUSPICIOUS_KEYWORDS):
        return 'suspicious'
    if path.endswith(('.php', '.asp', '.aspx', '.cgi', '.pl')):
        return 'suspicious'
    if any(path.endswith(ext) for ext in SAFE_EXTENSIONS) and not query:
        return 'safe_static'
    if 'bot' in ua or 'googlebot' in ua:
        return 'needs_review'
    return 'needs_review'

def apply_group_tagging(df):
    # Create a composite group key
    df['group_key'] = df['ip'] + '||' + df['user_agent']

    group_map = {}
    for key, group in df.groupby('group_key'):
        tags = group['whitelist_tag'].unique()
        if set(tags) == {'safe_static'}:
            group_map[key] = 'group_safe'
        else:
            group_map[key] = 'group_mixed'

    df['group_whitelist_tag'] = df['group_key'].map(group_map)
    df.drop(columns=['group_key'], inplace=True)
    return df



def main(input_path, output_path):
    print(f"Loading data from: {input_path}")
    df = pd.read_parquet(input_path)

    print("Tagging rows...")
    df['whitelist_tag'] = df.apply(tag_row, axis=1)

    print("Applying group-level logic...")
    df = apply_group_tagging(df)

    print(f"Saving tagged logs to: {output_path}")
    df.to_parquet(output_path, index=False)
    print("Done.")

    # --- Summary Report ---
    print("\nSummary:")
    print("Row-level whitelist tags:")
    print(df['whitelist_tag'].value_counts())

    print("\nGroup-level whitelist tags:")
    print(df['group_whitelist_tag'].value_counts())

    print("\nTop suspicious IPs:")
    suspicious_ips = (
        df[df['whitelist_tag'] == 'suspicious']
        .groupby('ip')
        .size()
        .sort_values(ascending=False)
        .head(10)
    )
    print(suspicious_ips)



input_file = "../ssl-logs/parquet/raw/ssl-access.log-20181001.parquet"
output_file = "../ssl-logs/parquet/whitelist/ssl-access.log-20181001.parquet"

main(input_file, output_file)
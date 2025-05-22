import pandas as pd
import re
from urllib.parse import urlparse, parse_qs
from datetime import datetime

from utils.log_summary import print_parse_summary


def parse_apache_log_line(line: str) -> dict:
    """
    Parse a single Apache SSL access log line (combined format with tls and cipher) into a dictionary.
    """

    # Adjust this pattern to match your format exactly
    log_pattern = re.compile(
        r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] '
        r'"(?P<request>.*?)" (?P<status>\d+) (?P<response_size>\S+) '
        r'"(?P<referrer>.*?)" "(?P<user_agent>.*?)" '
        r'(?P<tls>\S+) (?P<cipher>\S+)$'
    )

    match = log_pattern.match(line)
    if not match:
        return None

    d = match.groupdict()

    # Replace '-' with 0 for response_size
    d['response_size'] = int(d['response_size']) if d['response_size'].isdigit() else 0
    d['status'] = int(d['status'])

    # Parse and normalize timestamp
    d['timestamp'] = datetime.strptime(d['timestamp'], "%d/%b/%Y:%H:%M:%S %z")

    return d

def parse_apache_log_file(path: str, show_summary: bool = True) -> pd.DataFrame:
    """
        Read a raw Apache log file and return a cleaned DataFrame. Print summary.
    """

    parsed_rows = []
    failed_lines = []

    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            parsed = parse_apache_log_line(line.strip())
            if parsed:
                parsed_rows.append(parsed)
            else:
                failed_lines.append((i, line.strip()))

    if show_summary:
        print_parse_summary(total=i, parsed=len(parsed_rows), failed_lines=failed_lines)

    return pd.DataFrame(parsed_rows)


def save_parquet(df: pd.DataFrame, path: str):
    df.to_parquet(path, index=False)



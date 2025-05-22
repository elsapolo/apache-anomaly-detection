# utils/request_parser.py

import pandas as pd
from urllib.parse import urlparse, parse_qs


def parse_request_line(request_line: str) -> pd.Series:
    """
    Parses a single HTTP request line (e.g., "GET /index.html HTTP/1.1").
    Returns a Series with method, path, query string, and error flags.
    """
    try:
        parts = request_line.strip().split(" ")
        if len(parts) < 3:
            raise ValueError("Malformed request line")

        method = parts[0]
        http_version = parts[-1]
        url = " ".join(parts[1:-1])
        parsed_url = urlparse(url)

        path = parsed_url.path
        query_string = parsed_url.query

        try:
            query_dict = parse_qs(query_string, strict_parsing=False)
            query_error = False
        except Exception:
            query_dict = {}
            query_error = True

        return pd.Series({
            "method": method,
            "path": path,
            "query_string": query_string,
            "query_dict": query_dict,
            "http_version": http_version,
            "request_error": False,
            "query_error": query_error,
        })

    except Exception:
        return pd.Series({
            "method": None,
            "path": None,
            "query_string": None,
            "query_dict": None,
            "http_version": None,
            "request_error": True,
            "query_error": None,
        })


def parse_request_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies request line parsing to a DataFrame with a 'request' column.
    Adds new columns: method, path, query_string, query_dict, http_version,
    request_error, query_error.
    """
    if "request" not in df.columns:
        raise ValueError("Expected 'request' column in input DataFrame.")

    parsed = df["request"].apply(parse_request_line)
    return pd.concat([df, parsed], axis=1)


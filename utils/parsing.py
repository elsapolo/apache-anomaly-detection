import json

import pandas as pd


def parse_query_dict_string(s: str) -> dict:
    """
    Safely parses a query_dict_str column (JSON-encoded string) into a Python dict.
    Returns an empty dict if malformed or null.
    """
    try:
        return json.loads(s) if isinstance(s, str) and s != "null" else {}
    except Exception:
        return {}


def extract_query_keys(query_dict: dict) -> tuple:
    """
    Given a parsed query_dict (e.g., from parse_query_dict_string),
    returns a sorted tuple of the top-level keys.

    Returns an empty tuple if input is not a dict.
    """
    if isinstance(query_dict, dict):
        return tuple(sorted(query_dict.keys()))
    return tuple()

def parse_query_dict_string_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a 'query_dict' column to the DataFrame by parsing the JSON-formatted
    strings in the 'query_dict_str' column.
    """
    if "query_dict_str" not in df.columns:
        raise KeyError("Missing required column: 'query_dict_str'")

    df["query_dict"] = df["query_dict_str"].apply(parse_query_dict_string)
    return df

def extract_query_keys_df(df: pd.DataFrame) -> pd.DataFrame:
    """
        Adds a 'query_keys' column to the DataFrame from 'query_dict' column.
        Sorted tuple of top level query keys
        """
    if "query_dict" not in df.columns:
        raise KeyError("Missing required column: 'query_dict'")

    df["query_keys"] = df["query_dict"].apply(extract_query_keys)
    return df

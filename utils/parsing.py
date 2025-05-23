import json

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

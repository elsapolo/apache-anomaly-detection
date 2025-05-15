import pandas as pd
from urllib.parse import urlparse, parse_qs
import json

from extract_raw_logs import save_to_parquet


def parse_request_line(request_line):
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
            "query_error": query_error
        })

    except Exception as e:
        print(f"Failed to parse: {request_line} -> {e}")
        return pd.Series({
            "method": None,
            "path": None,
            "query_string": None,
            "query_dict": None,
            "http_version": None,
            "request_error": True,
            "query_error": None
        })



df = pd.read_parquet("../ssl-logs/parquet/raw/ssl-access.log-all.parquet")


# Apply parser to the request column
parsed = df["request"].apply(parse_request_line)

# Summary before merging
num_request_errors = parsed["request_error"].sum()
num_query_errors = parsed["query_error"].sum()

print("📊 Summary of Parsing:")
print(f"❌ Request parse failures: {num_request_errors}")
print(f"⚠️  Query parse failures (but request was okay): {num_query_errors}")
print(f"✅ Successfully parsed: {len(parsed) - num_request_errors}")


# Add the new parsed fields
df = pd.concat([df, parsed], axis=1)

df["query_dict_str"] = df["query_dict"].apply(lambda d: json.dumps(d) if isinstance(d, dict) else None)

# Drop the original request column
df = df.drop(columns=["request", "query_dict", "request_error", "query_error"])

save_to_parquet(df,"../ssl-logs/parquet/raw/ssl-access.log-all-url.parquet")

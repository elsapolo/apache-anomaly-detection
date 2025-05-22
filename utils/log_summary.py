def print_parse_summary(total: int, parsed: int, failed_lines: list, max_lines_to_show: int = 10):
    """
    Print a summary of parsing results and show a few failed lines.
    """
    failed_count = len(failed_lines)

    print(f"\n📊 Parsing Summary")
    print(f"Total lines processed: {total}")
    print(f"✅ Parsed successfully: {parsed}")
    print(f"❌ Failed to parse:     {failed_count}")

    if failed_count > 0:
        print(f"\n🔍 Failed Lines (showing up to {max_lines_to_show}):")
        for i, line in failed_lines[:max_lines_to_show]:
            print(f"[Line {i}]: {line}")
        if failed_count > max_lines_to_show:
            print(f"... {failed_count - max_lines_to_show} more not shown ...")



def print_request_parse_summary(df):
    """
    Prints a summary of request and query parsing results.
    Assumes the DataFrame contains 'request_error', 'query_error', 'request' and 'query string' columns.
    """
    if "request_error" not in df.columns or "query_error" not in df.columns:
        print("Missing 'request_error' or 'query_error' column in DataFrame.")
        return

    total = len(df)
    request_errors = df["request_error"].sum()
    query_errors = df["query_error"].sum()
    parsed_ok = total - request_errors - query_errors

    print("\n📊 Request Parsing Summary")
    print(f"Total records:              {total:,}")
    print(f"✅ Successfully parsed:     {parsed_ok:,}")
    print(f"❌ Request parse failures:  {request_errors:,}")
    print(f"⚠️ Query parse issues:      {query_errors:,}")

    if request_errors > 0:
        print(f"\n🔍 First 10 failed requests:")
        print(df[df["request_error"]].head(10)[["request"]])

    if query_errors > 0:
        print(f"\n🔍 First 10 failed queries:")
        print(df[df["request_error"]].head(10)[["query_string"]])

def print_whitelist_summary(df):
    """
    Prints a summary of whitelisting results.
    Assumes the DataFrame contains 'whitelisted' column.
    """

    if "whitelisted" not in df.columns:
        print("Missing 'whitelisted' column in DataFrame.")
        return

    total = len(df)
    whitelisted = df["whitelisted"].sum()
    not_whitelisted = total - whitelisted

    print("\n📊 Request Parsing Summary")
    print(f"Total records:              {total:,}")
    print(f"✅ Whitelisted:     {whitelisted:,}")
    print(f"❌ Not whitelisted parse failures:  {not_whitelisted:,}")

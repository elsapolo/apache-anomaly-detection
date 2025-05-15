import pandas as pd
from extract_raw_logs import save_to_parquet

# Define image and pdf extensions
image_pdf_exts = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.pdf')

# Read the log file
df = pd.read_parquet("../ssl-logs/parquet/raw/ssl-access.log-all-url.parquet")

# Define whitelisting conditions
is_status_200 = df['status'] == 200
is_get = df['method'] == 'GET'
no_query = df['query_string'] == ""
is_index_html = df['path'] == '/index.html'
is_image_pdf = df['path'].str.lower().str.endswith(image_pdf_exts)

# Combine conditions for whitelisting
df['whitelisted'] = is_status_200 & is_get & no_query & (is_index_html | is_image_pdf)


# Save non-whitelisted logs (without the flag column)
save_to_parquet(
    df[~df['whitelisted']].drop(columns=['whitelisted']),
    "../ssl-logs/parquet/raw/ssl-access.log-all-url-notWhitelisted.parquet"
)

# Summarize
num_index_html = df[df['whitelisted'] & is_index_html].shape[0]
num_image_pdf = df[df['whitelisted'] & is_image_pdf].shape[0]

print("📊 Summary of Whitelist:")
print(f"🟢 Whitelisted /index.html (no queries): {num_index_html}")
print(f"🖼️ Whitelisted image/pdf files (no queries): {num_image_pdf}")
print(f"✅ Total whitelisted: {df['whitelisted'].sum()}")
print(f"🚫 Total NOT whitelisted: {(~df['whitelisted']).sum()}")

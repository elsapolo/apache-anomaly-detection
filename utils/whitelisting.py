import pandas as pd

IMAGE_PDF_EXTS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.pdf')

def apply_whitelist(df: pd.DataFrame) -> pd.DataFrame:
    is_status_200 = df['status'] == 200
    is_get = df['method'] == 'GET'
    no_query = df['query_string'] == ""
    is_index_html = df['path'] == '/index.html'
    is_image_pdf = df['path'].str.lower().str.endswith(IMAGE_PDF_EXTS)

    df['whitelisted'] = is_status_200 & is_get & no_query & (is_index_html | is_image_pdf)
    return df

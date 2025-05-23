import pandas as pd
from utils.data_split import split_for_analysis
from utils.log_loading import save_parquet

def split_data(input_path, output_train, output_eval, ratio=0.8):
    df = pd.read_parquet(input_path)

    df_train, df_eval = split_for_analysis(df, ratio)

    save_parquet(df_train, output_train)
    save_parquet(df_eval, output_eval)


input_path = "../data/parsed/all_ssl_access-url-whitelisted.parquet"
output_train = "../data/split/whitelisted-80-20/all_ssl-access-url-whitelisted-train-80.parquet"
output_eval = "../data/split/whitelisted-80-20/all_ssl-access-url-whitelisted-eval-80.parquet"

split_data(input_path, output_train, output_eval)



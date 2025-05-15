import gzip
import re
import pandas as pd

#return df with access logs
def parse_access_log(file_path: str):
    # Define the Apache log format regex
    log_pattern = (
        r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>.*?)\] "(?P<request>.*?)" '
        r'(?P<status>\d+) (?P<size>\S+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)" '
        r'(?P<tls>.*?) (?P<cipher>.*?)'
    )

    # List to store parsed data
    parsed_data = []

    # Open the .gz file and parse
    with gzip.open(file_path, "rt") as file:
        for line in file:
            match = re.match(log_pattern, line)
            if match:
                log_data = match.groupdict()  # Extract structured data as a dictionary
                parsed_data.append(log_data)  # Append to the list
            else:
                print("ERROR: Invalid log format", line)
    # Convert to a pandas DataFrame
    df = pd.DataFrame(parsed_data)

    # Convert numeric fields and parse timestamp
    df['size'] = pd.to_numeric(df['size'], errors='coerce').fillna(0)
    df['status'] = pd.to_numeric(df['status'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z')


    # Display the DataFrame
    #print(df.head())

    return df

# Save the DataFrame to a JSON file
def save_to_json(df: pd.DataFrame, output_file: str):
    df.to_json(output_file, orient='records', lines=True)
    #print(f"Parsed logs saved to {output_file}")

def save_to_parquet(df: pd.DataFrame, output_file: str):
    df.to_parquet(output_file, engine="pyarrow", index=False)

#SAMPLE USAGE
#input_log_file = "../ssl-logs/ssl-access.log-20181001.gz"
#output_parquet_file = "../ssl-logs/parquet/raw/ssl-access.log-20181001.parquet"

#df = parse_access_log(input_log_file)
#save_to_parquet(df, output_parquet_file)


access_file_path = "../ssl-logs/"
gz_access_file = "ssl-access.log-"
year = 2018

df = pd.DataFrame()

for month in range(10,12):
    for day in range(1,32):
        if month == 11 and day == 31:
            continue
        if day < 10:
            day = "0" + str(day)
        filename = access_file_path + gz_access_file + str(year) + str(month) + str(day) + ".gz"
        df = pd.concat([df, parse_access_log(filename)], ignore_index=True)

print(df.head())


output_file = "../ssl-logs/parquet/raw/ssl-access.log-all.parquet"
save_to_parquet(df, output_file)
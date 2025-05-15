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
                print("ERROR: Invalid log format")
    # Convert to a pandas DataFrame
    df = pd.DataFrame(parsed_data)

    # Convert numeric fields and parse timestamp
    df['size'] = pd.to_numeric(df['size'], errors='coerce').fillna(0)
    df['status'] = pd.to_numeric(df['status'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z')


    # Display the DataFrame
    print(df.head())

    return df

#prints df, prints unmatched logs
def parse_error_log(file_path: str):

    # Pattern to extract fields from each log line
    pattern = r'\[(.*?)\] \[(.*?)\] \[pid (\d+):tid (\d+)\] \[client ([\d\.]+):(\d+)\] (AH\d+): (.+)'

    # Initialize a list to store parsed log entries
    parsed_logs = []
    unmatched_logs = []

    # Open and process the .gz file
    with gzip.open(file_path, 'rt') as file:
        for line in file:
            # Match the pattern against each line
            match = re.match(pattern, line)
            if match:
                parsed_logs.append(match.groups())
            else:
                unmatched_logs.append(line)

    # Convert parsed data to a DataFrame
    columns = ["Timestamp", "Log Level", "PID", "TID", "Client IP", "Client Port", "Code", "Message"]
    df = pd.DataFrame(parsed_logs, columns=columns)

    #Display unmatched logs
    if unmatched_logs:
        print("Unmatched Logs:")
        for log in unmatched_logs[:5]:  # Print the first few
            print(log)

    # Display the DataFrame
    print(df.head())

# Save the DataFrame to a JSON file
def save_to_json(df: pd.DataFrame, output_file: str):
    df.to_json(output_file, orient='records', lines=True)
    print(f"Parsed logs saved to {output_file}")

#prints first lines of gz file
def print_first_lines(file_path: str):
    """
    prints first lines of gz file
    :param file_path:
    :return:
    """
    with gzip.open(file_path, 'rt') as file:
        for i, line in enumerate(file):
            print(line.strip())
            if i == 9:  # Stop after 10 lines
                break

#elastic search from json file to json file with extra bit
def save_to_json_elasticsearch(input_file: str, output_file: str):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            outfile.write('{"index": {"_index": "apache-logs"}}\n')
            outfile.write(line)


#parse_error_log('../ssl-logs/ssl-error.log-20181001.gz')

input_log_file = "../ssl-logs/ssl-access.log-20181001.gz"
# Output JSON file path
output_json_file = "../ssl-logs/json/ssl-access.log-20181001.json"

# Parse logs and save to JSON
df = parse_access_log(input_log_file)
save_to_json(df, output_json_file)
save_to_json_elasticsearch(output_json_file, "../ssl-logs/json/elasticsearch/ssl-access.log-20181001.json")
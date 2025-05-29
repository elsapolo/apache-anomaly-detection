import argparse
import select
import subprocess, sys, tqdm
from itertools import islice

import pyarrow as pa, pyarrow.parquet as pq
import pandas as pd

"""
To run this you need to be inside the cloned wazuh-docker/single-node
  
You need to start the docker:
    docker-compose up -d

use this to check analysisd is running:
    docker ps
"""

NAME  = "wazuh-offline"
CHUNK_SIZE = 10000

def run(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()

def need_container():
    # Check if the container is running
    if not run(["docker", "ps", "-q", "-f", f"name={NAME}"]):
        sys.exit(f"container {NAME!r} is not running")

    # Check if wazuh-analysisd is running inside the container
    if not run(["docker", "exec", NAME, "pgrep", "-f", "wazuh-analysisd"]):
        sys.exit("analysisd inside the container is not running")


def main(file, out, limit):
    need_container()

    open("output.parquet", "wb").close()


    schema = pa.schema([
        ("line_number", pa.int32()),
        ("rule_id", pa.string()),
        ("level", pa.string()),
        ("description", pa.string()),
    ])
    writer = pq.ParquetWriter("labels.parquet", schema)
    buffer = []

    src = open(file)
    if limit is not None:
        src = islice(src, limit)

    logtest = subprocess.Popen(
        ["docker", "exec", "-i", NAME, "/var/ossec/bin/wazuh-logtest"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for ln, log in tqdm.tqdm(enumerate(src), desc="Processing", total=3500000):
        logtest.stdin.write(log)
        logtest.stdin.flush()

        phase_3 = False
        id_ = level = desc = None

        while not (phase_3 and id_ and desc and level):
            rlist, _, _ = select.select([logtest.stdout], [], [], 5)
            if not rlist:
                break

            s = logtest.stdout.readline()
           #print(repr(s))
            if s.startswith("**Phase 3"):
               #print("__________ PHASE 3")
                phase_3 = True                      # skip marker
            if phase_3:
                if s.startswith("\tid:"):
                    id_ = s.split("'")[1]
                   #print("------id", id_)
                elif s.startswith("\tlevel:"):
                    level = s.split("'")[1]
                   #print("------level", level)
                elif s.startswith("\tdescription:"):
                    desc = s.split("'")[1]
                    #print("------description", desc)


        buffer.append((ln, id_, level, desc))
        if len(buffer) >= CHUNK_SIZE:
            df = pd.DataFrame(buffer, columns=["line_number", "rule_id", "level", "description"])
            table = pa.Table.from_pandas(df, schema=schema)
            writer.write_table(table)
            buffer.clear()

    if buffer:
        df = pd.DataFrame(buffer, columns=["line_number", "rule_id", "level", "description"])
        table = pa.Table.from_pandas(df, schema=schema)
        writer.write_table(table)

    writer.close()

    # tidy up
    logtest.stdin.close()
    logtest.terminate()
    print(f"→ wrote {ln:,} rows to {out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--file",  required=True)
    ap.add_argument("--out",   default="labels.parquet")
    ap.add_argument("--limit", type=int)
    main(**vars(ap.parse_args()))

from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

db_dir = os.getenv("ROCKSDB_DIR")

def get_statistics(options = None):
    raw_results = get_raw_results(options)

    results = raw_results.split("\n")
    return results

def get_raw_results(options = None):
    command = [db_dir+"/db_bench",
                "--benchmarks=fillseq,stats",
                "--statistics"]
    try:
        result = subprocess.run(command,capture_output=True,text=True,check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing benchmark: {e}")
        print(e.stderr)
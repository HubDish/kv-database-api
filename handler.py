import os
import sys
import subprocess

db_dir = os.getcwd()+"/rocksdb"
sys.path.append(db_dir+"/tools/advisor")

from advisor.db_bench_runner import DBBenchRunner

def get_statistics(options = None):
    #raw_results = get_raw_results(options)
    #db_options = options_parser.DatabaseOptions('test/input_files/OPTIONS-000005')
    #print(db_options)

    results = raw_results.split("\n")
    return results

def get_raw_results(options = None):
    # command = [db_dir+"/db_bench",
    #             "--benchmarks=fillseq,stats",
    #             "--statistics"]
    command = [db_dir+"/db_bench",
                "--benchmarks=fillseq"]
    try:
        result = subprocess.run(command,capture_output=True,text=True,check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing benchmark: {e}")
        print(e.stderr)
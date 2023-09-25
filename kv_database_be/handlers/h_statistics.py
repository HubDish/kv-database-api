import os
import sys
import subprocess
from kv_database_be.log import logger
from kv_database_be.constants import avail_benchmarks, avail_options
from kv_database_be.utils import get_key_stats, get_db_path, split_output, prepare_statistics

cur_dir = os.getcwd()
db_dir = cur_dir+"/rocksdb"

def get_statistics(benchmark):
    raw_results = get_raw_results(benchmark)

    results = raw_results.split("\n")

    main, db_stats, statistics = split_output(raw_results)
    count_stats, graph_stats = prepare_statistics(statistics)
    # print(main)
    # print("Hi")
    # print(db_stats)
    # print("Hi")
    
    # print(raw_results)

    db_path = get_db_path(results)
    key_size = get_key_stats("Keys", "str", results)
    value_size = get_key_stats("Values", "str", results)
    no_entries = get_key_stats("Entries", "int", results)
    raw_size = get_key_stats("RawSize", "str", results)
    file_size = get_key_stats("FileSize", "str", results)
    
    
    output = {
        'db_path': db_path,
        'key_size': key_size,
        'value_size': value_size,
        'no_entries': no_entries,
        'raw_size': raw_size,
        'file_size': file_size,
        'count_stats': count_stats,
        'graph_stats': graph_stats
    }

    return output

def get_raw_results(benchmark):
    command = [db_dir+"/db_bench",
                "--benchmarks="+benchmark+",stats",
                "--statistics",
                "--options_file="+cur_dir+"/tmp_options.ini"]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing benchmark: {e}")
        print(e.stderr)
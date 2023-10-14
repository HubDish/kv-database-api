import os
import sys
import subprocess
from kv_database_be.log import logger
from kv_database_be.utils import get_key_stats, get_db_path, split_output, prepare_statistics, prepare_db_stats

cur_dir = os.getcwd()
db_dir = cur_dir+"/rocksdb"

def get_statistics(benchmark):
    try:
        # raw_results = get_raw_results(benchmark)
        # f=open("tmp_benchmark_stats.txt","w")
        # f.write(raw_results)
        # f.close()
        with open("tmp/fillsync_output.txt","r") as file:
            raw_results = file.read()

        main, db_stats, statistics = split_output(raw_results)
        count_stats, graph_stats = prepare_statistics(statistics)
        # print(main)
        # print("Hi")
        # print("Hi")
        db_stats = prepare_db_stats(db_stats)
        # print(raw_results)

        db_path = get_db_path(main)
        key_size = get_key_stats("Keys", "str", main)
        value_size = get_key_stats("Values", "str", main)
        no_entries = get_key_stats("Entries", "int", main)
        raw_size = get_key_stats("RawSize", "str", main)
        file_size = get_key_stats("FileSize", "str", main)
        
        output = {
            'db_path': db_path,
            'key_size': key_size,
            'value_size': value_size,
            'no_entries': no_entries,
            'raw_size': raw_size,
            'file_size': file_size,
            'db_stats': db_stats,
            'count_stats': count_stats,
            'graph_stats': graph_stats
        }

        return output
    except subprocess.CalledProcessError as e:
        logger.error(f"Error in benchmark: {e}")
        logger.error(f"stderr: {e.stderr}")

        output = {
            'error': True,
            'message': e.stderr
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
        raise e
import os
import subprocess
from kv_database_be.log import logger
from kv_database_be.utils import split_output, get_db_path, prepare_statistics, prepare_db_stats

cur_dir = os.getcwd()
db_dir = cur_dir+"/rocksdb"

def get_statistics(benchmark):
    try:
        raw_results = get_raw_results(benchmark)
        f=open("tmp_benchmark_stats.txt","w")
        f.write(raw_results)
        f.close()
        # with open("tmp/fillsync_output.txt","r") as file:
        #     raw_results = file.read()

        main, db_stats, statistics = split_output(raw_results)
        count_stats, graph_stats = prepare_statistics(statistics)
        db_stats = prepare_db_stats(db_stats)
        # print(raw_results)

        db_path = get_db_path(main)
        
        output = {
            'db_path': db_path,
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
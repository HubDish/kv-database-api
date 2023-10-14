from kv_database_be.log import logger
from kv_database_be.constants import avail_benchmarks, avail_options

def get_avail_benchmarks():
    list_of_benchmarks = []
    for key in avail_benchmarks:
        benchmark = {
            "label": key,
            "description": avail_benchmarks[key]
        }
        list_of_benchmarks.append(benchmark)
    return list_of_benchmarks

def get_avail_options():
    return avail_options

def create_options_file(content):
    f=open("tmp_options.ini","wb")
    f.write(content)
    f.close()
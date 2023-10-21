import re
from kv_database_be.log import logger

def split_output(raw_results):
    logger.info("Splitting RocksDB Raw Output")
    split_on = ["** DB Stats **", "STATISTICS:"]
    pattern = "|".join(map(re.escape, split_on))
    sections = re.split(pattern, raw_results)

    main = sections[0]
    db_stats = sections[1]
    statistics = sections[2]

    return main, db_stats, statistics

def get_key_stats(key, data_type, result):
    logger.info(f"Getting {key}")
    lines = result.strip().split('\n')
    line_req = [s for s in lines if key+":" in s][0]
    line_req = line_req.replace(key+":", "")
    line_req = line_req.strip(" \t")
    if data_type == "int":
        return int(line_req)
    else:
        return line_req

def get_db_path(result):
    logger.info("Getting DB Path")
    result = result.strip().split('\n')
    line_req = [s for s in result if "DB path:" in s][0]
    start_index = line_req.index("[") + 1
    end_index = line_req.index("]", start_index)
    return line_req[start_index:end_index]

def prepare_db_stats(db_stats):
    logger.info("Preparing DB Stats")
    lines = db_stats.strip().split('\n')
    result = {}
    for line in lines:
        if "Uptime(secs):" in line:
            pattern = r"Uptime\(secs\): (\d+\.\d+) total, (\d+\.\d+) interval"
            match = re.search(pattern, line)
            result["uptime"] = [float(match.group(1)), float(match.group(2))]
        if "Cumulative writes:" in line or "Interval writes:" in line:
            pattern = r"Cumulative writes: (\d+\.*\d*)([KM])* writes, (\d+\.*\d*)([KM])* keys, (\d+\.*\d*)([KM])* commit groups, (\d+\.*\d*) writes per commit group, ingest: (\d+\.*\d*) (\w+), (\d+\.*\d*) (\w+)/s"
            if "Interval writes:" in line:
                pattern = r"Interval writes: (\d+\.*\d*)([KM])* writes, (\d+\.*\d*)([KM])* keys, (\d+\.*\d*)([KM])* commit groups, (\d+\.*\d*) writes per commit group, ingest: (\d+\.*\d*) (\w+), (\d+\.*\d*) (\w+)/s"
            match = re.search(pattern, line)
            write_data = {}
            
            # Number of writes
            write_data["no_writes"] = int(match.group(1))
            if match.group(2) == "K":
                write_data["no_writes"] = write_data["no_writes"]*1000
            elif match.group(2) == "M":
                write_data["no_writes"] = write_data["no_writes"]*1000*1000

            # Number of keys
            write_data["no_keys"] = int(match.group(3))
            if match.group(4) == "K":
                write_data["no_keys"] = write_data["no_keys"]*1000
            elif match.group(4) == "M":
                write_data["no_keys"] = write_data["no_keys"]*1000*1000
            
            # Commit Groups
            write_data["no_commit_groups"] = int(match.group(5))
            if match.group(6) == "K":
                write_data["no_commit_groups"] = write_data["no_commit_groups"]*1000
            elif match.group(6) == "M":
                write_data["no_commit_groups"] = write_data["no_commit_groups"]*1000*1000

            # Writes per Commit Group
            write_data["writes_per_commit_group"] = float(match.group(7))
            
            # Ingest Size
            write_data["ingest_size"] = float(match.group(8))
            if match.group(9) == "KB":
                write_data["ingest_size"] = write_data["ingest_size"]*1024
            elif match.group(9) == "MB":
                write_data["ingest_size"] = write_data["ingest_size"]*1024*1024
            elif match.group(9) == "GB":
                write_data["ingest_size"] = write_data["ingest_size"]*1024*1024*1024
            
            # Ingest Rate
            write_data["ingest_rate"] = float(match.group(10))
            if match.group(11) == "KB":
                write_data["ingest_rate"] = write_data["ingest_rate"]*1024
            elif match.group(11) == "MB":
                write_data["ingest_rate"] = write_data["ingest_rate"]*1024*1024
            elif match.group(11) == "GB":
                write_data["ingest_rate"] = write_data["ingest_rate"]*1024*1024*1024
            
            if "Cumulative writes:" in line:
                result["cumulative_writes"] = write_data
            else:
                result["interval_writes"] = write_data
        if "Cumulative WAL:" in line or "Interval WAL:" in line:
            pattern = r"Cumulative WAL: (\d+\.*\d*)([KM])* writes, (\d+\.*\d*)([KM])* syncs, (\d+\.*\d*) writes per sync, written: (\d+\.*\d*) (\w+), (\d+\.*\d*) (\w+)/s"
            if "Interval WAL:" in line:
                pattern = r"Interval WAL: (\d+\.*\d*)([KM])* writes, (\d+\.*\d*)([KM])* syncs, (\d+\.*\d*) writes per sync, written: (\d+\.*\d*) (\w+), (\d+\.*\d*) (\w+)/s"
            
            match = re.search(pattern, line)
            wal_data = {}
            
            # Number of writes
            wal_data["no_writes"] = int(match.group(1))
            if match.group(2) == "K":
                wal_data["no_writes"] = wal_data["no_writes"]*1000
            elif match.group(2) == "M":
                wal_data["no_writes"] = wal_data["no_writes"]*1000*1000

            # Number of syncs
            wal_data["no_syncs"] = int(match.group(3))
            if match.group(4) == "K":
                wal_data["no_syncs"] = wal_data["no_syncs"]*1000
            elif match.group(4) == "M":
                wal_data["no_syncs"] = wal_data["no_syncs"]*1000*1000
            
            # Number of writes per sync
            wal_data["writes_per_sync"] = float(match.group(5))
            
            # Written size
            wal_data["written_size"] = float(match.group(6))
            if match.group(7) == "KB":
                wal_data["written_size"] = wal_data["written_size"]*1024
            elif match.group(7) == "MB":
                wal_data["written_size"] = wal_data["written_size"]*1024*1024
            elif match.group(7) == "GB":
                wal_data["written_size"] = wal_data["written_size"]*1024*1024*1024
            
            # Written rate
            wal_data["written_rate"] = float(match.group(8))
            if match.group(9) == "KB":
                wal_data["written_rate"] = wal_data["written_rate"]*1024
            elif match.group(9) == "MB":
                wal_data["written_rate"] = wal_data["written_rate"]*1024*1024
            elif match.group(9) == "GB":
                wal_data["written_rate"] = wal_data["written_rate"]*1024*1024*1024
            
            if "Cumulative WAL:" in line:
                result["cumulative_wal"] = wal_data
            else:
                result["interval_wal"] = wal_data
        if "Cumulative stall:" in line or "Interval stall:" in line:
            pattern = r'Cumulative stall: (\d+:\d+:\d+\.\d+) H:M:S, (\d+\.\d+) percent'
            if "Interval stall:" in line:
                pattern = r'Interval stall: (\d+:\d+:\d+\.\d+) H:M:S, (\d+\.\d+) percent'
            
            match = re.search(pattern, line)
            stall_data = {}
            
            # Stall time
            stall_data["time"] = match.group(1)

            # Stall percent
            stall_data["percent"] = float(match.group(2))
            
            if "Cumulative stall:" in line:
                result["cumulative_stall"] = stall_data
            else:
                result["interval_stall"] = stall_data
            
    return result


def prepare_statistics(statistics):
    logger.info("Preparing In-Depth Statistics")
    pattern = r'(?=rocksdb\.db\.get\.micros)'
    sections = re.split(pattern, statistics)
    count_stats = sections[0]
    graph_stats = sections[1]

    count_stats = clean_statistics("COUNT", count_stats)
    graph_stats = clean_statistics("GRAPH", graph_stats)

    return count_stats, graph_stats

def clean_statistics(stats_type, statistics):
    logger.info("Cleaning In-Depth Statistics")
    lines = statistics.strip().split('\n')
    results = []
    if stats_type == "COUNT":
        filtered_lines = [line for line in lines if "COUNT : 0" not in line]
        for line in filtered_lines:
            split_string = line.split('COUNT : ')
            id = split_string[0].strip()
            value = int(split_string[1])

            #Clean up title
            title = id.replace('rocksdb.', '')
            title = title.replace('.', ' ')
            title = title.title()

            results.append({
                'id': id,
                'title': title,
                'value': value
            })
    else:
        filtered_lines = [line for line in lines if "SUM : 0" not in line]
        for line in filtered_lines:
            tokens = line.split()
            id = tokens[0].strip()
            percentiles = []
            yaxis = ''
            count = 0
            sum_val = 0

            #Clean up title
            title = id.replace('rocksdb.', '')
            title = title.replace('.', ' ')
            title = title.title()

            if 'Micros' in title:
                yaxis = 'Latency (ms)'
                title = title.replace('Micros', '').strip()

            if 'Bytes' in title:
                yaxis = 'Bytes'

            for i in range(1, len(tokens), 3):
                key = tokens[i]
                value = float(tokens[i + 2])

                if key == 'P50':
                    percentiles.append(value)
                elif key == 'P95':
                    percentiles.append(value)
                elif key == 'P99':
                    percentiles.append(value)
                elif key == 'P100':
                    percentiles.append(value)
                elif key == 'COUNT':
                    count = value
                elif key == 'SUM':
                    sum_val = value

            results.append({
                'id': id,
                'title': title,
                'yaxis': yaxis,
                'count': count,
                'sum': sum_val,
                'percentiles': percentiles
            })

    return results

def clean_rule(rule):
    cleaned_rule = {}
    cleaned_rule["rule"] = rule["rule"].strip()
    cleaned_rule["title"] = cleaned_rule["rule"].replace('-', ' ')
    cleaned_rule["title"] = cleaned_rule["title"].title()

    cleaned_rule["suggestions"] = []
    pattern = r"Suggestion: (\S+) option : (\S+) action : (\w+)(?: suggested_values : \[([^\]]+)\])?"

    for suggestion in rule["suggestions"]:
        logger.info(suggestion)
        match = re.search(pattern, suggestion)
        suggestion_info = {
            "suggestion": match.group(1),
            "title": match.group(1),
            "option": match.group(2),
            "action": match.group(3),
        }
        suggested_values = match.group(4)
        suggestion_info["suggestion"] = suggestion_info["suggestion"].strip()

        suggestion_info["title"] = suggestion_info["suggestion"].replace('-', ' ')
        suggestion_info["title"] = suggestion_info["title"].replace('inc', 'increase')
        suggestion_info["title"] = suggestion_info["title"].replace('dec', 'decrease')
        suggestion_info["title"] = suggestion_info["title"].replace('bg', 'background')
        suggestion_info["title"] = suggestion_info["title"].title()

        suggestion_info["action"] = suggestion_info["action"].title()

        if suggested_values is not None:
            suggestion_info["suggested_values"] = suggested_values.split(', ')
        cleaned_rule["suggestions"].append(suggestion_info)

    return cleaned_rule


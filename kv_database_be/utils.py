import re

def get_key_stats(key, data_type, result):
    line_req = [s for s in result if key+":" in s][0]
    line_req = line_req.replace(key+":", "")
    line_req = line_req.strip(" \t")
    if data_type == "int":
        return int(line_req)
    else:
        return line_req

def get_db_path(result):
    line_req = [s for s in result if "DB path:" in s][0]
    start_index = line_req.index("[") + 1
    end_index = line_req.index("]", start_index)
    return line_req[start_index:end_index]

def split_output(raw_results):
    split_on = ["** DB Stats **", "STATISTICS:"]
    pattern = "|".join(map(re.escape, split_on))
    sections = re.split(pattern, raw_results)

    main = sections[0]
    db_stats = sections[1]
    statistics = sections[2]

    return main, db_stats, statistics

def prepare_statistics(statistics):
    pattern = r'(?=rocksdb\.db\.get\.micros)'
    sections = re.split(pattern, statistics)
    count_stats = sections[0]
    graph_stats = sections[1]

    count_stats = clean_statistics("COUNT", count_stats)
    graph_stats = clean_statistics("GRAPH", graph_stats)

    return count_stats, graph_stats

def clean_statistics(stats_type, statistics):
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

def get_db_path(result):
    print(result)
    line_req = [s for s in result if "DB path:" in s][0]
    start_index = line_req.index("[") + 1
    end_index = line_req.index("]", start_index)
    return line_req[start_index:end_index]
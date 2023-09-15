avail_benchmarks = {
    "fillseq": "write N values in sequential key order in async mode",
    "fillseqdeterministic": "write N values in the specified key order and keep the shape of the LSM tree",
    "fillrandom": "write N values in random key order in async mode",
    "filluniquerandomdeterministic": "write N values in a random key order and keep the shape of the LSM tree",
    "overwrite": "overwrite N values in random key order in async mode",
    "fillsync": "write N/100 values in random key order in sync mode",
    "fill100K": "write N/1000 100K values in random order in async mode",
    "deleteseq": "delete N keys in sequential order",
    "deleterandom": "delete N keys in random order",
    "readseq": "read N times sequentially",
    "readtocache": "1 thread reading database sequentially",
    "readreverse": "read N times in reverse order",
    "readrandom": "read N times in random order",
    "readmissing": "read N missing keys in random order",
    "readwhilewriting": "1 writer, N threads doing random reads",
    "readwhilemerging": "1 merger, N threads doing random reads",
    "readrandomwriterandom" : "N threads doing random-read, random-write",
    "prefixscanrandom": "prefix scan N times in random order",
    "updaterandom": "N threads doing read-modify-write for random keys",
    "appendrandom": "N threads doing read-modify-write with growing values",
    "mergerandom": "same as updaterandom/appendrandom using merge operator. Must be used with merge_operator",
    "readrandommergerandom": "perform N random read-or-merge operations. Must be used with merge_operator",
    "newiterator": "repeated iterator creation",
    "seekrandom": "N random seeks, call Next seek_nexts times per seek",
    "seekrandomwhilewriting": "seekrandom and 1 thread doing overwrite",
    "seekrandomwhilemerging": "seekrandom and 1 thread doing merge",
    "crc32c": "repeated crc32c of 4K of data",
    "xxhash": "repeated xxHash of 4K of data",
    "acquireload": "load N*1000 times",
    "fillseekseq": "write N values in sequential key, then read them by seeking to each key",
    "randomtransaction": "execute N random transactions and verify correctness",
    "randomreplacekeys": "randomly replaces N keys by deleting the old version and putting the new version",
    "timeseries": "1 writer generates time series data and multiple readers doing random reads on id",
}

avail_options = {
    "DBOptions": [
        {
            "name": "max_open_files",
            "description": """
                Number of open files that can be used by the DB.  You may need to\n
                increase this if your database has a large working set. Value -1 means\n
                files opened are always kept open. You can estimate number of files based\n
                on target_file_size_base and target_file_size_multiplier for level-based\n
                compaction. For universal-style compaction, you can usually set it to -1.\n
                \n
                A high value or -1 for this option can cause high memory usage.
            """,
            "type": "int",
            "default": -1
        },
        {
            "name": "max_file_opening_threads",
            "description": """
                If max_open_files is -1, DB will open all files on DB::Open(). You can\n
                use this option to increase the number of threads used to open the files.
            """,
            "type": "int",
            "default": 16
        },
        {
            "name": "max_total_wal_size",
            "description": """
                Once write-ahead logs exceed this size, we will start forcing the flush of\n
                column families whose memtables are backed by the oldest live WAL file\n
                (i.e. the ones that are causing all the space amplification). If set to 0\n
                (default), we will dynamically choose the WAL size limit to be\n
                [sum of all write_buffer_size * max_write_buffer_number] * 4\n
                \n
                For example, with 15 column families, each with\n
                write_buffer_size = 128 MB\n
                max_write_buffer_number = 6\n
                max_total_wal_size will be calculated to be [15 * 128MB * 6] * 4 = 45GB\n
                \n
                This option takes effect only when there are more than one column\n
                family as otherwise the wal size is dictated by the write_buffer_size.
            """,
            "type": "int",
            "default": 0
        },
        {
            "name": "stats_dump_period_sec",
            "description": """
                if not zero, dump rocksdb.stats to LOG every stats_dump_period_sec
            """,
            "type": "int",
            "default": 600
        },
        {
            "name": "max_manifest_file_size",
            "description": """
                manifest file is rolled over on reaching this limit.\n
                The older manifest file be deleted.\n
                The default value is 1GB so that the manifest file can grow, but not\n
                reach the limit of storage capacity.
            """,
            "type": "int",
            "default": 1024*1024*1024
        },
        {
            "name": "",
            "description": "",
            "type": "",
            "default": ""
        }
    ]
}
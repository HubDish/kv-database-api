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
            "name": "create_if_missing",
            "description": "If true, the database will be created if it is missing.",
            "type": "bool",
            "default": False
        },
        {
            "name": "create_missing_column_families",
            "description": "If true, missing column families will be automatically created.",
            "type": "bool",
            "default": False
        },
        {
            "name": "error_if_exists",
            "description": "If true, an error is raised if the database already exists.",
            "type": "bool",
            "default": False
        },
        {
            "name": "paranoid_checks",
            "description": ("If true, RocksDB will aggressively check consistency of the data.\n"
                "Also, if any of the  writes to the database fails (Put, Delete, Merge,\n"
                "Write), the database will switch to read-only mode and fail all other\n"
                "Write operations.\n"
                "In most cases you want this to be set to true."),
            "type": "bool",
            "default": True
        },
        {
            "name": "flush_verify_memtable_count",
            "description": ("If true, during memtable flush, RocksDB will validate total entries\n"
                "read in flush, and compare with counter inserted into it.\n"
                "\n"
                "The option is here to turn the feature off in case this new validation\n"
                "feature has a bug. The option may be removed in the future once the\n"
                "feature is stable."),
            "type": "bool",
            "default": True
        },
        {
            "name": "compaction_verify_record_count",
            "description": ("If true, during compaction, RocksDB will count the number of entries\n"
                "read and compare it against the number of entries in the compaction\n"
                "input files. This is intended to add protection against corruption\n"
                "during compaction. Note that\n"
                "- this verification is not done for compactions during which a compaction\n"
                "filter returns kRemoveAndSkipUntil, and\n"
                "- the number of range deletions is not verified.\n"
                "\n"
                "The option is here to turn the feature off in case this new validation\n"
                "feature has a bug. The option may be removed in the future once the\n"
                "feature is stable."),
            "type": "bool",
            "default": True
        },
        {
            "name": "track_and_verify_wals_in_manifest",
            "description": ("If true, the log numbers and sizes of the synced WALs are tracked\n"
                "in MANIFEST. During DB recovery, if a synced WAL is missing\n"
                "from disk, or the WAL's size does not match the recorded size in\n"
                "MANIFEST, an error will be reported and the recovery will be aborted.\n"
                "\n"
                "This is one additional protection against WAL corruption besides the\n"
                "per-WAL-entry checksum.\n"
                "\n"
                "Note that this option does not work with secondary instance.\n"
                "Currently, only syncing closed WALs are tracked. Calling `DB::SyncWAL()`,\n"
                "etc. or writing with `WriteOptions::sync=true` to sync the live WAL is not\n"
                "tracked for performance/efficiency reasons."),
            "type": "bool",
            "default": False
        },
        {
            "name": "verify_sst_unique_id_in_manifest",
            "description": ("If true, verifies the SST unique id between MANIFEST and actual file\n"
                "each time an SST file is opened. This check ensures an SST file is not\n"
                "overwritten or misplaced. A corruption error will be reported if mismatch\n"
                "detected, but only when MANIFEST tracks the unique id, which starts from\n"
                "RocksDB version 7.3. Although the tracked internal unique id is related\n"
                "to the one returned by GetUniqueIdFromTableProperties, that is subject to\n"
                "change.\n"
                "NOTE: verification is currently only done on SST files using block-based\n"
                "table format.\n"
                "\n"
                "Setting to false should only be needed in case of unexpected problems.\n"
                "\n"
                "Although an early version of this option opened all SST files for\n"
                "verification on DB::Open, that is no longer guaranteed. However, as\n"
                "documented in an above option, if max_open_files is -1, DB will open all\n"
                "files on DB::Open()."),
            "type": "bool",
            "default": True
        },
        {
            "name": "max_open_files",
            "description": ("Number of open files that can be used by the DB. You may need to\n"
                "increase this if your database has a large working set. Value -1 means\n"
                "files opened are always kept open. You can estimate number of files based\n"
                "on target_file_size_base and target_file_size_multiplier for level-based\n"
                "compaction. For universal-style compaction, you can usually set it to -1.\n"
                "\n"
                "A high value or -1 for this option can cause high memory usage."),
            "type": "int",
            "default": -1
        },
        {
            "name": "max_file_opening_threads",
            "description": ("If max_open_files is -1, DB will open all files on DB::Open(). You can\n"
                "use this option to increase the number of threads used to open the files."),
            "type": "int",
            "default": 16
        },
        {
            "name": "max_total_wal_size",
            "description": ("Once write-ahead logs exceed this size, we will start forcing the flush of\n"
                "column families whose memtables are backed by the oldest live WAL file\n"
                "(i.e. the ones that are causing all the space amplification). If set to 0\n"
                "(default), we will dynamically choose the WAL size limit to be\n"
                "[sum of all write_buffer_size * max_write_buffer_number] * 4\n"
                "\n"
                "For example, with 15 column families, each with\n"
                "write_buffer_size = 128 MB\n"
                "max_write_buffer_number = 6\n"
                "max_total_wal_size will be calculated to be [15 * 128MB * 6] * 4 = 45GB\n"
                "\n"
                "This option takes effect only when there are more than one column\n"
                "family as otherwise the wal size is dictated by the write_buffer_size."),
            "type": "int",
            "default": 0
        },
        {
            "name": "use_fsync",
            "description": ("By default, writes to stable storage use fdatasync (on platforms\n"
                "where this function is available). If this option is true,\n"
                "fsync is used instead.\n"
                "\n"
                "fsync and fdatasync are equally safe for our purposes and fdatasync is\n"
                "faster, so it is rarely necessary to set this option. It is provided\n"
                "as a workaround for kernel/filesystem bugs, such as one that affected\n"
                "fdatasync with ext4 in kernel versions prior to 3.7."),
            "type": "bool",
            "default": False
        },
        {
            "name": "stats_dump_period_sec",
            "description": "if not zero, dump rocksdb.stats to LOG every stats_dump_period_sec",
            "type": "int",
            "default": 600
        },
        {
            "name": "max_manifest_file_size",
            "description": ("manifest file is rolled over on reaching this limit.\n"
                "The older manifest file be deleted.\n"
                "The default value is 1GB so that the manifest file can grow, but not\n"
                "reach the limit of storage capacity."),
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
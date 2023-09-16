// The periodicity when obsolete files get deleted. The default
// value is 6 hours. The files that get out of scope by compaction
// process will still get automatically delete on every compaction,
// regardless of this setting
//
// Default: 6 hours
//
// Dynamically changeable through SetDBOptions() API.
uint64_t delete_obsolete_files_period_micros = 6ULL * 60 * 60 * 1000000;

// Maximum number of concurrent background jobs (compactions and flushes).
//
// Default: 2
//
// Dynamically changeable through SetDBOptions() API.
int max_background_jobs = 2;

// DEPRECATED: RocksDB automatically decides this based on the
// value of max_background_jobs. For backwards compatibility we will set
// `max_background_jobs = max_background_compactions + max_background_flushes`
// in the case where user sets at least one of `max_background_compactions` or
// `max_background_flushes` (we replace -1 by 1 in case one option is unset).
//
// Maximum number of concurrent background compaction jobs, submitted to
// the default LOW priority thread pool.
//
// If you're increasing this, also consider increasing number of threads in
// LOW priority thread pool. For more information, see
// Env::SetBackgroundThreads
//
// Default: -1
//
// Dynamically changeable through SetDBOptions() API.
int max_background_compactions = -1;

// This value represents the maximum number of threads that will
// concurrently perform a compaction job by breaking it into multiple,
// smaller ones that are run simultaneously.
// Default: 1 (i.e. no subcompactions)
//
// Dynamically changeable through SetDBOptions() API.
uint32_t max_subcompactions = 1;

// DEPRECATED: RocksDB automatically decides this based on the
// value of max_background_jobs. For backwards compatibility we will set
// `max_background_jobs = max_background_compactions + max_background_flushes`
// in the case where user sets at least one of `max_background_compactions` or
// `max_background_flushes`.
//
// Maximum number of concurrent background memtable flush jobs, submitted by
// default to the HIGH priority thread pool. If the HIGH priority thread pool
// is configured to have zero threads, flush jobs will share the LOW priority
// thread pool with compaction jobs.
//
// It is important to use both thread pools when the same Env is shared by
// multiple db instances. Without a separate pool, long running compaction
// jobs could potentially block memtable flush jobs of other db instances,
// leading to unnecessary Put stalls.
//
// If you're increasing this, also consider increasing number of threads in
// HIGH priority thread pool. For more information, see
// Env::SetBackgroundThreads
// Default: -1
int max_background_flushes = -1;

// Specify the maximal size of the info log file. If the log file
// is larger than `max_log_file_size`, a new info log file will
// be created.
// If max_log_file_size == 0, all logs will be written to one
// log file.
size_t max_log_file_size = 0;

// Time for the info log file to roll (in seconds).
// If specified with non-zero value, log file will be rolled
// if it has been active longer than `log_file_time_to_roll`.
// Default: 0 (disabled)
size_t log_file_time_to_roll = 0;

// Maximal info log files to be kept.
// Default: 1000
size_t keep_log_file_num = 1000;

// Recycle log files.
// If non-zero, we will reuse previously written log files for new
// logs, overwriting the old data.  The value indicates how many
// such files we will keep around at any point in time for later
// use.  This is more efficient because the blocks are already
// allocated and fdatasync does not need to update the inode after
// each write.
// Default: 0
size_t recycle_log_file_num = 0;

// manifest file is rolled over on reaching this limit.
// The older manifest file be deleted.
// The default value is 1GB so that the manifest file can grow, but not
// reach the limit of storage capacity.
uint64_t max_manifest_file_size = 1024 * 1024 * 1024;

// Number of shards used for table cache.
int table_cache_numshardbits = 6;

// The following two fields affect how archived logs will be deleted.
// 1. If both set to 0, logs will be deleted asap and will not get into
//    the archive.
// 2. If WAL_ttl_seconds is 0 and WAL_size_limit_MB is not 0,
//    WAL files will be checked every 10 min and if total size is greater
//    then WAL_size_limit_MB, they will be deleted starting with the
//    earliest until size_limit is met. All empty files will be deleted.
// 3. If WAL_ttl_seconds is not 0 and WAL_size_limit_MB is 0, then
//    WAL files will be checked every WAL_ttl_seconds / 2 and those that
//    are older than WAL_ttl_seconds will be deleted.
// 4. If both are not 0, WAL files will be checked every 10 min and both
//    checks will be performed with ttl being first.
uint64_t WAL_ttl_seconds = 0;
uint64_t WAL_size_limit_MB = 0;

// Number of bytes to preallocate (via fallocate) the manifest
// files.  Default is 4mb, which is reasonable to reduce random IO
// as well as prevent overallocation for mounts that preallocate
// large amounts of data (such as xfs's allocsize option).
size_t manifest_preallocation_size = 4 * 1024 * 1024;

// Allow the OS to mmap file for reading sst tables.
// Not recommended for 32-bit OS.
// When the option is set to true and compression is disabled, the blocks
// will not be copied and will be read directly from the mmap-ed memory
// area, and the block will not be inserted into the block cache. However,
// checksums will still be checked if ReadOptions.verify_checksums is set
// to be true. It means a checksum check every time a block is read, more
// than the setup where the option is set to false and the block cache is
// used. The common use of the options is to run RocksDB on ramfs, where
// checksum verification is usually not needed.
// Default: false
bool allow_mmap_reads = false;

// Allow the OS to mmap file for writing.
// DB::SyncWAL() only works if this is set to false.
// Default: false
bool allow_mmap_writes = false;

// Enable direct I/O mode for read/write
// they may or may not improve performance depending on the use case
//
// Files will be opened in "direct I/O" mode
// which means that data r/w from the disk will not be cached or
// buffered. The hardware buffer of the devices may however still
// be used. Memory mapped files are not impacted by these parameters.

// Use O_DIRECT for user and compaction reads.
// Default: false
bool use_direct_reads = false;

// Use O_DIRECT for writes in background flush and compactions.
// Default: false
bool use_direct_io_for_flush_and_compaction = false;

// If false, fallocate() calls are bypassed, which disables file
// preallocation. The file space preallocation is used to increase the file
// write/append performance. By default, RocksDB preallocates space for WAL,
// SST, Manifest files, the extra space is truncated when the file is written.
// Warning: if you're using btrfs, we would recommend setting
// `allow_fallocate=false` to disable preallocation. As on btrfs, the extra
// allocated space cannot be freed, which could be significant if you have
// lots of files. More details about this limitation:
// https://github.com/btrfs/btrfs-dev-docs/blob/471c5699336e043114d4bca02adcd57d9dab9c44/data-extent-reference-counts.md
bool allow_fallocate = true;

// Disable child process inherit open files. Default: true
bool is_fd_close_on_exec = true;

// if not zero, dump rocksdb.stats to LOG every stats_dump_period_sec
//
// Default: 600 (10 min)
//
// Dynamically changeable through SetDBOptions() API.
unsigned int stats_dump_period_sec = 600;

// if not zero, dump rocksdb.stats to RocksDB every stats_persist_period_sec
// Default: 600
unsigned int stats_persist_period_sec = 600;

// If true, automatically persist stats to a hidden column family (column
// family name: ___rocksdb_stats_history___) every
// stats_persist_period_sec seconds; otherwise, write to an in-memory
// struct. User can query through `GetStatsHistory` API.
// If user attempts to create a column family with the same name on a DB
// which have previously set persist_stats_to_disk to true, the column family
// creation will fail, but the hidden column family will survive, as well as
// the previously persisted statistics.
// When peristing stats to disk, the stat name will be limited at 100 bytes.
// Default: false
bool persist_stats_to_disk = false;

// if not zero, periodically take stats snapshots and store in memory, the
// memory size for stats snapshots is capped at stats_history_buffer_size
// Default: 1MB
size_t stats_history_buffer_size = 1024 * 1024;

// If set true, will hint the underlying file system that the file
// access pattern is random, when a sst file is opened.
// Default: true
bool advise_random_on_open = true;

// Amount of data to build up in memtables across all column
// families before writing to disk.
//
// This is distinct from write_buffer_size, which enforces a limit
// for a single memtable.
//
// This feature is disabled by default. Specify a non-zero value
// to enable it.
//
// Default: 0 (disabled)
size_t db_write_buffer_size = 0;

// The memory usage of memtable will report to this object. The same object
// can be passed into multiple DBs and it will track the sum of size of all
// the DBs. If the total size of all live memtables of all the DBs exceeds
// a limit, a flush will be triggered in the next DB to which the next write
// is issued, as long as there is one or more column family not already
// flushing.
//
// If the object is only passed to one DB, the behavior is the same as
// db_write_buffer_size. When write_buffer_manager is set, the value set will
// override db_write_buffer_size.
//
// This feature is disabled by default. Specify a non-zero value
// to enable it.
//
// Default: null
std::shared_ptr<WriteBufferManager> write_buffer_manager = nullptr;

// Specify the file access pattern once a compaction is started.
// It will be applied to all input files of a compaction.
// Default: NORMAL
enum AccessHint { NONE, NORMAL, SEQUENTIAL, WILLNEED };
AccessHint access_hint_on_compaction_start = NORMAL;

// If non-zero, we perform bigger reads when doing compaction. If you're
// running RocksDB on spinning disks, you should set this to at least 2MB.
// That way RocksDB's compaction is doing sequential instead of random reads.
//
// Default: 0
//
// Dynamically changeable through SetDBOptions() API.
size_t compaction_readahead_size = 0;

// This is a maximum buffer size that is used by WinMmapReadableFile in
// unbuffered disk I/O mode. We need to maintain an aligned buffer for
// reads. We allow the buffer to grow until the specified value and then
// for bigger requests allocate one shot buffers. In unbuffered mode we
// always bypass read-ahead buffer at ReadaheadRandomAccessFile
// When read-ahead is required we then make use of compaction_readahead_size
// value and always try to read ahead. With read-ahead we always
// pre-allocate buffer to the size instead of growing it up to a limit.
//
// This option is currently honored only on Windows
//
// Default: 1 Mb
//
// Special value: 0 - means do not maintain per instance buffer. Allocate
//                per request buffer and avoid locking.
size_t random_access_max_buffer_size = 1024 * 1024;

// This is the maximum buffer size that is used by WritableFileWriter.
// With direct IO, we need to maintain an aligned buffer for writes.
// We allow the buffer to grow until it's size hits the limit in buffered
// IO and fix the buffer size when using direct IO to ensure alignment of
// write requests if the logical sector size is unusual
//
// Default: 1024 * 1024 (1 MB)
//
// Dynamically changeable through SetDBOptions() API.
size_t writable_file_max_buffer_size = 1024 * 1024;

// Use adaptive mutex, which spins in the user space before resorting
// to kernel. This could reduce context switch when the mutex is not
// heavily contended. However, if the mutex is hot, we could end up
// wasting spin time.
// Default: false
bool use_adaptive_mutex = false;

// Create DBOptions with default values for all fields
DBOptions();
// Create DBOptions from Options
explicit DBOptions(const Options& options);

void Dump(Logger* log) const;

// Allows OS to incrementally sync files to disk while they are being
// written, asynchronously, in the background. This operation can be used
// to smooth out write I/Os over time. Users shouldn't rely on it for
// persistence guarantee.
// Issue one request for every bytes_per_sync written. 0 turns it off.
//
// You may consider using rate_limiter to regulate write rate to device.
// When rate limiter is enabled, it automatically enables bytes_per_sync
// to 1MB.
//
// This option applies to table files
//
// Default: 0, turned off
//
// Note: DOES NOT apply to WAL files. See wal_bytes_per_sync instead
// Dynamically changeable through SetDBOptions() API.
uint64_t bytes_per_sync = 0;

// Same as bytes_per_sync, but applies to WAL files
//
// Default: 0, turned off
//
// Dynamically changeable through SetDBOptions() API.
uint64_t wal_bytes_per_sync = 0;

// When true, guarantees WAL files have at most `wal_bytes_per_sync`
// bytes submitted for writeback at any given time, and SST files have at most
// `bytes_per_sync` bytes pending writeback at any given time. This can be
// used to handle cases where processing speed exceeds I/O speed during file
// generation, which can lead to a huge sync when the file is finished, even
// with `bytes_per_sync` / `wal_bytes_per_sync` properly configured.
//
//  - If `sync_file_range` is supported it achieves this by waiting for any
//    prior `sync_file_range`s to finish before proceeding. In this way,
//    processing (compression, etc.) can proceed uninhibited in the gap
//    between `sync_file_range`s, and we block only when I/O falls behind.
//  - Otherwise the `WritableFile::Sync` method is used. Note this mechanism
//    always blocks, thus preventing the interleaving of I/O and processing.
//
// Note: Enabling this option does not provide any additional persistence
// guarantees, as it may use `sync_file_range`, which does not write out
// metadata.
//
// Default: false
bool strict_bytes_per_sync = false;

// A vector of EventListeners whose callback functions will be called
// when specific RocksDB event happens.
std::vector<std::shared_ptr<EventListener>> listeners;

// If true, then the status of the threads involved in this DB will
// be tracked and available via GetThreadList() API.
//
// Default: false
bool enable_thread_tracking = false;

// The limited write rate to DB if soft_pending_compaction_bytes_limit or
// level0_slowdown_writes_trigger is triggered, or we are writing to the
// last mem table allowed and we allow more than 3 mem tables. It is
// calculated using size of user write requests before compression.
// RocksDB may decide to slow down more if the compaction still
// gets behind further.
// If the value is 0, we will infer a value from `rater_limiter` value
// if it is not empty, or 16MB if `rater_limiter` is empty. Note that
// if users change the rate in `rate_limiter` after DB is opened,
// `delayed_write_rate` won't be adjusted.
//
// Unit: byte per second.
//
// Default: 0
//
// Dynamically changeable through SetDBOptions() API.
uint64_t delayed_write_rate = 0;

// By default, a single write thread queue is maintained. The thread gets
// to the head of the queue becomes write batch group leader and responsible
// for writing to WAL and memtable for the batch group.
//
// If enable_pipelined_write is true, separate write thread queue is
// maintained for WAL write and memtable write. A write thread first enter WAL
// writer queue and then memtable writer queue. Pending thread on the WAL
// writer queue thus only have to wait for previous writers to finish their
// WAL writing but not the memtable writing. Enabling the feature may improve
// write throughput and reduce latency of the prepare phase of two-phase
// commit.
//
// Default: false
bool enable_pipelined_write = false;

// Setting unordered_write to true trades higher write throughput with
// relaxing the immutability guarantee of snapshots. This violates the
// repeatability one expects from ::Get from a snapshot, as well as
// ::MultiGet and Iterator's consistent-point-in-time view property.
// If the application cannot tolerate the relaxed guarantees, it can implement
// its own mechanisms to work around that and yet benefit from the higher
// throughput. Using TransactionDB with WRITE_PREPARED write policy and
// two_write_queues=true is one way to achieve immutable snapshots despite
// unordered_write.
//
// By default, i.e., when it is false, rocksdb does not advance the sequence
// number for new snapshots unless all the writes with lower sequence numbers
// are already finished. This provides the immutability that we expect from
// snapshots. Moreover, since Iterator and MultiGet internally depend on
// snapshots, the snapshot immutability results into Iterator and MultiGet
// offering consistent-point-in-time view. If set to true, although
// Read-Your-Own-Write property is still provided, the snapshot immutability
// property is relaxed: the writes issued after the snapshot is obtained (with
// larger sequence numbers) will be still not visible to the reads from that
// snapshot, however, there still might be pending writes (with lower sequence
// number) that will change the state visible to the snapshot after they are
// landed to the memtable.
//
// Default: false
bool unordered_write = false;

// If true, allow multi-writers to update mem tables in parallel.
// Only some memtable_factory-s support concurrent writes; currently it
// is implemented only for SkipListFactory.  Concurrent memtable writes
// are not compatible with inplace_update_support or filter_deletes.
// It is strongly recommended to set enable_write_thread_adaptive_yield
// if you are going to use this feature.
//
// Default: true
bool allow_concurrent_memtable_write = true;

// If true, threads synchronizing with the write batch group leader will
// wait for up to write_thread_max_yield_usec before blocking on a mutex.
// This can substantially improve throughput for concurrent workloads,
// regardless of whether allow_concurrent_memtable_write is enabled.
//
// Default: true
bool enable_write_thread_adaptive_yield = true;

// The maximum limit of number of bytes that are written in a single batch
// of WAL or memtable write. It is followed when the leader write size
// is larger than 1/8 of this limit.
//
// Default: 1 MB
uint64_t max_write_batch_group_size_bytes = 1 << 20;

// The maximum number of microseconds that a write operation will use
// a yielding spin loop to coordinate with other write threads before
// blocking on a mutex.  (Assuming write_thread_slow_yield_usec is
// set properly) increasing this value is likely to increase RocksDB
// throughput at the expense of increased CPU usage.
//
// Default: 100
uint64_t write_thread_max_yield_usec = 100;

// The latency in microseconds after which a std::this_thread::yield
// call (sched_yield on Linux) is considered to be a signal that
// other processes or threads would like to use the current core.
// Increasing this makes writer threads more likely to take CPU
// by spinning, which will show up as an increase in the number of
// involuntary context switches.
//
// Default: 3
uint64_t write_thread_slow_yield_usec = 3;

// If true, then DB::Open() will not update the statistics used to optimize
// compaction decision by loading table properties from many files.
// Turning off this feature will improve DBOpen time especially in
// disk environment.
//
// Default: false
bool skip_stats_update_on_db_open = false;

// If true, then DB::Open() will not fetch and check sizes of all sst files.
// This may significantly speed up startup if there are many sst files,
// especially when using non-default Env with expensive GetFileSize().
// We'll still check that all required sst files exist.
// If paranoid_checks is false, this option is ignored, and sst files are
// not checked at all.
//
// Default: false
bool skip_checking_sst_file_sizes_on_db_open = false;

// Recovery mode to control the consistency while replaying WAL
// Default: kPointInTimeRecovery
WALRecoveryMode wal_recovery_mode = WALRecoveryMode::kPointInTimeRecovery;

// if set to false then recovery will fail when a prepared
// transaction is encountered in the WAL
bool allow_2pc = false;

// A global cache for table-level rows.
// Default: nullptr (disabled)
std::shared_ptr<RowCache> row_cache = nullptr;

// A filter object supplied to be invoked while processing write-ahead-logs
// (WALs) during recovery. The filter provides a way to inspect log
// records, ignoring a particular record or skipping replay.
// The filter is invoked at startup and is invoked from a single-thread
// currently.
WalFilter* wal_filter = nullptr;

// If true, then DB::Open / CreateColumnFamily / DropColumnFamily
// SetOptions will fail if options file is not properly persisted.
//
// DEFAULT: false
bool fail_if_options_file_error = false;

// If true, then print malloc stats together with rocksdb.stats
// when printing to LOG.
// DEFAULT: false
bool dump_malloc_stats = false;

// By default RocksDB replay WAL logs and flush them on DB open, which may
// create very small SST files. If this option is enabled, RocksDB will try
// to avoid (but not guarantee not to) flush during recovery. Also, existing
// WAL logs will be kept, so that if crash happened before flush, we still
// have logs to recover from.
//
// DEFAULT: false
bool avoid_flush_during_recovery = false;

// By default RocksDB will flush all memtables on DB close if there are
// unpersisted data (i.e. with WAL disabled) The flush can be skip to speedup
// DB close. Unpersisted data WILL BE LOST.
//
// DEFAULT: false
//
// Dynamically changeable through SetDBOptions() API.
bool avoid_flush_during_shutdown = false;

// Set this option to true during creation of database if you want
// to be able to ingest behind (call IngestExternalFile() skipping keys
// that already exist, rather than overwriting matching keys).
// Setting this option to true has the following effects:
// 1) Disable some internal optimizations around SST file compression.
// 2) Reserve the last level for ingested files only.
// 3) Compaction will not include any file from the last level.
// Note that only Universal Compaction supports allow_ingest_behind.
// `num_levels` should be >= 3 if this option is turned on.
//
//
// DEFAULT: false
// Immutable.
bool allow_ingest_behind = false;

// If enabled it uses two queues for writes, one for the ones with
// disable_memtable and one for the ones that also write to memtable. This
// allows the memtable writes not to lag behind other writes. It can be used
// to optimize MySQL 2PC in which only the commits, which are serial, write to
// memtable.
bool two_write_queues = false;

// If true WAL is not flushed automatically after each write. Instead it
// relies on manual invocation of FlushWAL to write the WAL buffer to its
// file.
bool manual_wal_flush = false;

// If true, RocksDB supports flushing multiple column families and committing
// their results atomically to MANIFEST. Note that it is not
// necessary to set atomic_flush to true if WAL is always enabled since WAL
// allows the database to be restored to the last persistent state in WAL.
// This option is useful when there are column families with writes NOT
// protected by WAL.
// For manual flush, application has to specify which column families to
// flush atomically in DB::Flush.
// For auto-triggered flush, RocksDB atomically flushes ALL column families.
//
// Currently, any WAL-enabled writes after atomic flush may be replayed
// independently if the process crashes later and tries to recover.
bool atomic_flush = false;

// If true, working thread may avoid doing unnecessary and long-latency
// operation (such as deleting obsolete files directly or deleting memtable)
// and will instead schedule a background job to do it.
// Use it if you're latency-sensitive.
// If set to true, takes precedence over
// ReadOptions::background_purge_on_iterator_cleanup.
bool avoid_unnecessary_blocking_io = false;

// Historically DB ID has always been stored in Identity File in DB folder.
// If this flag is true, the DB ID is written to Manifest file in addition
// to the Identity file. By doing this 2 problems are solved
// 1. We don't checksum the Identity file where as Manifest file is.
// 2. Since the source of truth for DB is Manifest file DB ID will sit with
//    the source of truth. Previously the Identity file could be copied
//    independent of Manifest and that can result in wrong DB ID.
// We recommend setting this flag to true.
// Default: false
bool write_dbid_to_manifest = false;

// The number of bytes to prefetch when reading the log. This is mostly useful
// for reading a remotely located log, as it can save the number of
// round-trips. If 0, then the prefetching is disabled.
//
// Default: 0
size_t log_readahead_size = 0;

// If user does NOT provide the checksum generator factory, the file checksum
// will NOT be used. A new file checksum generator object will be created
// when a SST file is created. Therefore, each created FileChecksumGenerator
// will only be used from a single thread and so does not need to be
// thread-safe.
//
// Default: nullptr
std::shared_ptr<FileChecksumGenFactory> file_checksum_gen_factory = nullptr;

// By default, RocksDB will attempt to detect any data losses or corruptions
// in DB files and return an error to the user, either at DB::Open time or
// later during DB operation. The exception to this policy is the WAL file,
// whose recovery is controlled by the wal_recovery_mode option.
//
// Best-efforts recovery (this option set to true) signals a preference for
// opening the DB to any point-in-time valid state for each column family,
// including the empty/new state, versus the default of returning non-WAL
// data losses to the user as errors. In terms of RocksDB user data, this
// is like applying WALRecoveryMode::kPointInTimeRecovery to each column
// family rather than just the WAL.
//
// Best-efforts recovery (BER) is specifically designed to recover a DB with
// files that are missing or truncated to some smaller size, such as the
// result of an incomplete DB "physical" (FileSystem) copy. BER can also
// detect when an SST file has been replaced with a different one of the
// same size (assuming SST unique IDs are tracked in DB manifest).
// BER is not yet designed to produce a usable DB from other corruptions to
// DB files (which should generally be detectable by DB::VerifyChecksum()),
// and BER does not yet attempt to recover any WAL files.
//
// For example, if an SST or blob file referenced by the MANIFEST is missing,
// BER might be able to find a set of files corresponding to an old "point in
// time" version of the column family, possibly from an older MANIFEST
// file. Some other kinds of DB files (e.g. CURRENT, LOCK, IDENTITY) are
// either ignored or replaced with BER, or quietly fixed regardless of BER
// setting. BER does require at least one valid MANIFEST to recover to a
// non-trivial DB state, unlike `ldb repair`.
//
// Currently, best_efforts_recovery=true is not compatible with atomic flush.
//
// Default: false
bool best_efforts_recovery = false;

// It defines how many times DB::Resume() is called by a separate thread when
// background retryable IO Error happens. When background retryable IO
// Error happens, SetBGError is called to deal with the error. If the error
// can be auto-recovered (e.g., retryable IO Error during Flush or WAL write),
// then db resume is called in background to recover from the error. If this
// value is 0 or negative, DB::Resume() will not be called automatically.
//
// Default: INT_MAX
int max_bgerror_resume_count = INT_MAX;

// If max_bgerror_resume_count is >= 2, db resume is called multiple times.
// This option decides how long to wait to retry the next resume if the
// previous resume fails and satisfy redo resume conditions.
//
// Default: 1000000 (microseconds).
uint64_t bgerror_resume_retry_interval = 1000000;

// It allows user to opt-in to get error messages containing corrupted
// keys/values. Corrupt keys, values will be logged in the
// messages/logs/status that will help users with the useful information
// regarding affected data. By default value is set false to prevent users
// data to be exposed in the logs/messages etc.
//
// Default: false
bool allow_data_in_errors = false;

// A string identifying the machine hosting the DB. This
// will be written as a property in every SST file written by the DB (or
// by offline writers such as SstFileWriter and RepairDB). It can be useful
// for troubleshooting in memory corruption caused by a failing host when
// writing a file, by tracing back to the writing host. These corruptions
// may not be caught by the checksum since they happen before checksumming.
// If left as default, the table writer will substitute it with the actual
// hostname when writing the SST file. If set to an empty string, the
// property will not be written to the SST file.
//
// Default: hostname
std::string db_host_id = kHostnameForDbHostId;

// Use this if your DB want to enable checksum handoff for specific file
// types writes. Make sure that the File_system you use support the
// crc32c checksum verification
// Currently supported file tyes: kWALFile, kTableFile, kDescriptorFile.
// NOTE: currently RocksDB only generates crc32c based checksum for the
// handoff. If the storage layer has different checksum support, user
// should enble this set as empty. Otherwise,it may cause unexpected
// write failures.
FileTypeSet checksum_handoff_file_types;

// EXPERIMENTAL
// CompactionService is a feature allows the user to run compactions on a
// different host or process, which offloads the background load from the
// primary host.
// It's an experimental feature, the interface will be changed without
// backward/forward compatibility support for now. Some known issues are still
// under development.
std::shared_ptr<CompactionService> compaction_service = nullptr;

// It indicates, which lowest cache tier we want to
// use for a certain DB. Currently we support volatile_tier and
// non_volatile_tier. They are layered. By setting it to kVolatileTier, only
// the block cache (current implemented volatile_tier) is used. So
// cache entries will not spill to secondary cache (current
// implemented non_volatile_tier), and block cache lookup misses will not
// lookup in the secondary cache. When kNonVolatileBlockTier is used, we use
// both block cache and secondary cache.
//
// Default: kNonVolatileBlockTier
CacheTier lowest_used_cache_tier = CacheTier::kNonVolatileBlockTier;

// If set to false, when compaction or flush sees a SingleDelete followed by
// a Delete for the same user key, compaction job will not fail.
// Otherwise, compaction job will fail.
// This is a temporary option to help existing use cases migrate, and
// will be removed in a future release.
// Warning: do not set to false unless you are trying to migrate existing
// data in which the contract of single delete
// (https://github.com/facebook/rocksdb/wiki/Single-Delete) is not enforced,
// thus has Delete mixed with SingleDelete for the same user key. Violation
// of the contract leads to undefined behaviors with high possibility of data
// inconsistency, e.g. deleted old data become visible again, etc.
bool enforce_single_del_contracts = true;
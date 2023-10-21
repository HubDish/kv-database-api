import os
import sys
from kv_database_be.log import logger
from kv_database_be.utils import clean_rule

cur_dir = os.getcwd()
db_dir = cur_dir+"/rocksdb"
adv_dir = db_dir+"/tools/advisor"
sys.path.append(adv_dir)

from advisor.db_bench_runner import DBBenchRunner
from advisor.rule_parser import RulesSpec
from advisor.db_log_parser import DatabaseLogs, DataSource
from advisor.db_options_parser import DatabaseOptions
from advisor.db_stats_fetcher import LogStatsParser, OdsStatsFetcher

import json

def get_advice(db_path = None):
    raw_advice = get_raw_advice(db_path)
    # with open("sample_advice.txt","r") as file:
    #     raw_advice = json.load(file)
    cleaned_advice = []

    for rule in raw_advice:
        cleaned_advice.append(clean_rule(rule))

    return cleaned_advice

def get_raw_advice(db_path = None):
    # Taken from RocksDB Advisor rule_parser_example with minor modifications
    # initialise the RulesSpec parser
    rule_spec_parser = RulesSpec(adv_dir+"/advisor/rules.ini")
    rule_spec_parser.load_rules_from_spec()
    rule_spec_parser.perform_section_checks()

    # initialize the DatabaseOptions object
    # db_options = DatabaseOptions(adv_dir+"/test/input_files/OPTIONS-000005") #To change
    db_options = DatabaseOptions(db_path+"/OPTIONS-000007") #To change

    # Create DatabaseLogs object
    # db_logs = DatabaseLogs(adv_dir+"/test/input_files/LOG-0", db_options.get_column_families())
    db_logs = DatabaseLogs(db_path+"/LOG", db_options.get_column_families())

    # Create the Log STATS object
    # db_log_stats = LogStatsParser(adv_dir+"/test/input_files/LOG-0", 20)
    db_log_stats = LogStatsParser("/tmp/rocksdbtest-1000/dbbench/LOG", 20)
    data_sources = {
        DataSource.Type.DB_OPTIONS: [db_options],
        DataSource.Type.LOG: [db_logs],
        DataSource.Type.TIME_SERIES: [db_log_stats],
    }
    triggered_rules = rule_spec_parser.get_triggered_rules(
        data_sources, db_options.get_column_families()
    )

    cleaned_rules = []

    for rule in triggered_rules:
        add_rule = {}
        add_rule["rule"] = rule.name
        add_rule["conditions"] = []
        add_rule["suggestions"] = []
        add_rule["scope"] = []
        for cond_name in rule.conditions:
            add_rule["conditions"].append(repr(rule_spec_parser.conditions_dict[cond_name]))
        for sugg_name in rule.suggestions:
            add_rule["suggestions"].append(repr(rule_spec_parser.suggestions_dict[sugg_name]))
        if rule.trigger_entities:
            add_rule["scope"].append(rule.trigger_entities)
        if rule.trigger_column_families:
            add_rule["scope"].append(rule.trigger_column_families)
        cleaned_rules.append(add_rule)

    return cleaned_rules
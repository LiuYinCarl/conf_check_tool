import os
from pydoc import isdata
import sys
import builtins
import importlib
import json
from flask import Flask, request

root_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.append(root_dir)
import src.config as config
import src.server.rule_mgr as rule_mgr
from src.server.base import (log_init, debug_log, info_log, warn_log,
                             error_log, clear_cache_log, read_log,
                             read_cache_log)

def reg_builtins():
    """把 RuleMgr 单例注册到 bulitins 模块."""
    RULEMGR: rule_mgr.RuleMgr = rule_mgr.RuleMgr()
    if hasattr(builtins, "RM"):
        error_log("[ERROR] 'RM' already in builtins module.")
    setattr(builtins, "RM", RULEMGR)

    setattr(builtins, "debug_log", debug_log)
    setattr(builtins, "info_log", info_log)
    setattr(builtins, "warn_log", warn_log)
    setattr(builtins, "error_log", error_log)

def reg_config_tables():
    for path in config.SVR_DATA_DIR:
        if os.path.isdir(path):
            debug_log("[CONFIG TABLE DIR] {}".format(path))
            sys.path.append(path)
        elif os.path.isfile(path):
            debug_log("[CONFIG TABLE FILE] {}".format(path))
            sys.path.append(path)
        else:
            error_log("Unknown path: {}".format(path))

def reg_rule_modules():
    rule_modules = []
    rule_package = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "rules"))
    for file in os.listdir(rule_package):
        if os.path.isfile(os.path.join(rule_package, file)) and os.path.splitext(file)[-1] == ".py":
            rule_group_name = os.path.splitext(file)[0]
            module_name = "src.server.rules.{}".format(rule_group_name)
            debug_log("[IMPORT MODULR] {}".format(module_name))
            rule_modules.append((rule_group_name, module_name))

    for (rule_group_name, module_name) in rule_modules:
        importlib.import_module(module_name)
        RM.add_rule(rule_group_name, module_name)


app = Flask(__name__)

@app.route("/req_rule_group")
def on_req_rule_group():
    groups = RM.get_groups()
    data = {"rule_groups": groups}
    msg = json.dumps(data)
    return msg

@app.route("/check_rule", methods=["POST"])
def on_check_rule():
    clear_cache_log()
    req_params = request.form
    rule_groups = req_params.get("rule_groups")
    RM.exec_groups(rule_groups)
    log = read_cache_log()
    log_data = {"text_log": log}
    msg = json.dumps(log_data)
    return msg

@app.route("/sync_log")
def on_req_log():
    log = read_log()
    log_data = {"total_log": log}
    msg = json.dumps(log_data)
    return msg


def init():
    # 不要调整这里代码的顺序
    log_init()
    reg_builtins()
    reg_config_tables()
    reg_rule_modules()
    # RM.exec_rules()

if __name__ == "__main__":
    init()
    app.run(
        host = "127.0.0.1",
        port = 8000,
        debug = True
    )
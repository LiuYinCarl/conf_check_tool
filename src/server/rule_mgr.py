import os
import logging
from typing import Callable

import src.server.base as base
import src.common as common

@common.Singleton
class RuleMgr(object):
    """Config table check rules manager."""
    def __init__(self) -> None:
        self.check_rules = {}
        self.rules = {} # k:v = rule_name: module_name

    def add_rule(self, rule_group_name:str, module_name:str):
        self.rules[rule_group_name] = module_name

    def get_groups(self) -> list:
        groups = [group for group in self.rules.keys()]
        return groups

    def exec_groups(self, rule_groups:list) -> int:
        print(" rule_groups = {} check_rules = {}".format(rule_groups, self.check_rules.keys()))
        if not rule_groups: return
        executed_rule_names = set()
        for rg in rule_groups:
            for rule_name, func in self.check_rules.items():
                if rg in rule_name:
                    if rule_name in executed_rule_names: continue
                    executed_rule_names.add(rule_name)
                    try:
                        base.info_log("{}".format(rule_name))
                        res = func()
                        if not res:
                            base.error_log("[EXECUTE FAILED] {}".format(rule_name))
                    except Exception as e:
                        logging.exception(e)

    def reg_check_rule(self):
        """装饰器，用于注册配置表检查规则."""
        def decorator(func:Callable):
            file_name = os.path.normcase(func.__code__.co_filename)
            file_name = os.path.basename(file_name)
            module_name = os.path.splitext(file_name)[0]
            func_name = func.__name__

            if not hasattr(func, '__call__'):
                base.error_log("{}:{} is not function.".format(module_name, func_name))
            base.info_log("[REGIST CHECK RULE] {}:{}".format(module_name, func_name))

            rule_name = "{}:{}".format(module_name, func_name)
            self.check_rules[rule_name] = func
            return func

        return decorator

    def exec_rules(self) -> None:
        for rule_name, func in self.check_rules.items():
            try:
                res = func()
                if not res:
                    base.error_log("{}".format(rule_name))
                else:
                    base.info_log("{}".format(rule_name))
            except Exception as e:
                logging.exception(e)

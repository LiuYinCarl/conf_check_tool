import os
import logging
import src.server.base as base


@base.Singleton
class RuleMgr(object):
    """配置表规则检查器."""
    def __init__(self) -> None:
        self.check_rules = {}
        self.rules = {} # rule_name: module_name


    def add_rule(self, rule_group_name:str, module_name:str):
        self.rules[rule_group_name] = module_name

    def get_groups(self) -> list:
        groups = [group for group in self.rules.keys()]
        return groups

    def exec_group(self, rule_group_name:str) -> int:
        for rule_name, func in self.check_rules.items():
            print(" rule_group_name = {} rule_name = {}".format(rule_group_name, rule_name))
            if rule_group_name in rule_name:
                try:
                    res = func()
                    if not res:
                        error_log("{}".format(rule_name))
                    else:
                        info_log("{}".format(rule_name))
                except Exception as e:
                    logging.exception(e)

    def reg_check_rule(self):
        """装饰器，用于注册配置表检查规则."""
        def decorator(func):
            file_name = os.path.basename(__file__)
            func_name = func.__name__

            if not hasattr(func, '__call__'):
                error_log("{}:{} is not function.".format(file_name, func_name))
            info_log("[REGIST CHECK RULE] {}:{}".format(file_name, func_name))

            rule_name = "{}:{}".format(file_name, func_name)
            self.check_rules[rule_name] = func
            return func

        return decorator

    def exec_rules(self) -> None:
        for rule_name, func in self.check_rules.items():
            try:
                res = func()
                if not res:
                    error_log("{}".format(rule_name))
                else:
                    info_log("{}".format(rule_name))
            except Exception as e:
                logging.exception(e)

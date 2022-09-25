import os
import sys
import time
import logging
from typing import Callable

import src.common as common

# typing
t_log_func = Callable[[str, str, tuple], bool]

LOG_BUFFER = []

def log_cache() -> Callable:
    """ a decorator, used to append log into memory cache when
        call log function.
    """
    def cache(func:t_log_func) -> t_log_func:
        def wrapper(caller_msg:str, fmt:str, *args:tuple):
            log_level:str = func.__name__.split("_")[0].upper()
            msg:str = "{} {} {}".format(log_level, caller_msg, fmt % args)
            append_cache_log(msg)
            func(caller_msg, fmt, *args)
        return wrapper
    return cache

def show_caller(level=1) -> Callable:
    """ a decorator, used to append caller's infomation when
        call log function.
    """
    def show(func:t_log_func) -> t_log_func:
        def wrapper(*args, **kwargs):
            frame = sys._getframe(1)
            caller_info = "{}:{}:{}".format(frame.f_code.co_filename,
                                            frame.f_code.co_name,
                                            frame.f_lineno)
            func(caller_info, *args, **kwargs)
        return wrapper
    return show

def setup_logger(logger_name, log_file, level=logging.DEBUG):
    log:logging.Logger = logging.getLogger(logger_name)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    log.setLevel(level)
    log.addHandler(file_handler)
    log.addHandler(stream_handler)

def log_init():
    log_file = common.get_server_rule_log_file_path()
    if os.path.exists(log_file):
        clear_log()
    setup_logger("rule_log", log_file)

def append_cache_log(log:str):
    t:str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log = "{} {}".format(t, log)
    LOG_BUFFER.append(log)

def clear_cache_log():
    LOG_BUFFER.clear()

def clear_log():
    LOG_BUFFER.clear()
    log_file = common.get_server_rule_log_file_path()
    with open(log_file, 'w') as _: pass

def read_cache_log() -> str:
    log = "\n".join(LOG_BUFFER)
    return log

def read_log() -> str:
    log_file = common.get_server_rule_log_file_path()
    log = ""
    with open(log_file, "r") as f:
        log = "".join(f.readlines())
    return log

@show_caller()
@log_cache()
def debug_log(caller_msg, fmt, *args):
    msg = "{} {}".format(caller_msg, fmt % args)
    logging.getLogger("rule_log").debug(msg)

@show_caller()
@log_cache()
def info_log(caller_msg, fmt, *args):
    msg = "{} {}".format(caller_msg, fmt % args)
    logging.getLogger("rule_log").info(msg)

@show_caller()
@log_cache()
def warn_log(caller_msg, fmt, *args):
    msg = "{} {}".format(caller_msg, fmt % args)
    logging.getLogger("rule_log").warn(msg)

@show_caller()
@log_cache()
def error_log(caller_msg, fmt, *args):
    msg = "{} {}".format(caller_msg, fmt % args)
    logging.getLogger("rule_log").error(msg)
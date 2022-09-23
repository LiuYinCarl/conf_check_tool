import os
import sys
import time
import logging


class Singleton(object):
    """单例装饰器."""
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}
    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]

def log_cache():
    def cache(func):
        def wrapper(caller_msg, fmt, *args):
            log_level = func.__name__.split("_")[0].upper()
            msg = "{} {} {}".format(log_level, caller_msg, fmt % args)
            append_cache_log(msg)
            func(caller_msg, fmt, *args)
        return wrapper
    return cache

# 装饰器
def show_caller(level=1):
    def show(func):
        def wrapper(*args, **kwargs):
            caller_msg = '{0.f_code.co_filename}:{0.f_code.co_name}:{0.f_lineno}'.format(sys._getframe(level))
            func(caller_msg, *args, **kwargs)
        return wrapper
    return show

def _get_log_file_path() -> str:
    server_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "../"))
    log_file = os.path.join(server_dir, "check_config_tables.log")
    return log_file

def setup_logger(logger_name, log_file, level=logging.DEBUG):
    log = logging.getLogger(logger_name)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    log.setLevel(level)
    log.addHandler(file_handler)
    log.addHandler(stream_handler)

def log_init():
    log_file = _get_log_file_path()
    if os.path.exists(log_file):
        clear_log()
    setup_logger("conf_check_log", log_file)

log_buffer = []

def append_cache_log(log:str):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log = "{} {}".format(t, log)
    log_buffer.append(log)

def clear_cache_log():
    log_buffer.clear()

def clear_log():
    log_buffer.clear()
    log_file = _get_log_file_path()
    with open(log_file, 'w') as _: pass

def read_cache_log() -> str:
    log = "\n".join(log_buffer)
    # print(" ----- server cache log: ", log)
    return log

def read_log() -> str:
    log_file = _get_log_file_path()
    log = ""
    with open(log_file, "r") as f:
        log = "".join(f.readlines())
    # print("---- server total log: ", log)
    return log

@show_caller(1)
@log_cache()
def debug_log(caller_msg, fmt, *args):
    msg = "{} {}".format(caller_msg, fmt % args)
    logging.getLogger("conf_check_log").debug(msg)

@show_caller(1)
@log_cache()
def info_log(caller_msg, fmt, *args):
    msg = "{} {}".format(caller_msg, fmt % args)
    logging.getLogger("conf_check_log").info(msg)

@show_caller(1)
@log_cache()
def warn_log(caller_msg, fmt, *args):
    msg = "{} {}".format(caller_msg, fmt % args)
    logging.getLogger("conf_check_log").warn(msg)

@show_caller(1)
@log_cache()
def error_log(caller_msg, fmt, *args):
    msg = "{} {}".format(caller_msg, fmt % args)
    logging.getLogger("conf_check_log").error(msg)
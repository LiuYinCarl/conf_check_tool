import os
import sys
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

def log_init():
    log_file = _get_log_file_path()
    if os.path.exists(log_file):
        clear_log()

    logging.basicConfig(level=logging.DEBUG, #控制台打印的日志级别
                        filename=log_file,
                        filemode="a",
                        format="%(asctime)s %(levelname)s %(message)s")
                        # format="%(asctime)s %(pathname)s:%(lineno)d %(levelname)s %(message)s")

log_buffer = []

def clear_log():
    log_buffer.clear()
    log_file = _get_log_file_path()
    with open(log_file, 'w') as f:
        pass


def read_log() -> str:
    log = "\n".join(log_buffer)
    print(len(log_buffer))
    print(" ----- log: ", log)
    return log
    # log_file = _get_log_file_path()
    # ctx = ""
    # with open(log_file, "r") as f:
    #     ctx = "".join(f.readlines())
    # print("---- ctx: ", ctx)
    # return ctx

@show_caller(1)
def debug_log(caller_msg, fmt, *args):
    msg = "{} {}".format(caller_msg, fmt % args)
    log_buffer.append(msg)
    logging.debug(msg)

@show_caller(1)
def info_log(caller_msg, fmt, *args):
    msg = "{} {}".format(caller_msg, fmt % args)
    log_buffer.append(msg)
    logging.info(msg)

@show_caller(1)
def warn_log(caller_msg, fmt, *args):
    msg = "{} {}".format(caller_msg, fmt % args)
    log_buffer.append(msg)
    logging.warn(msg)

@show_caller(1)
def error_log(caller_msg, fmt, *args):
    msg = "{} {}".format(caller_msg, fmt % args)
    log_buffer.append(msg)
    logging.error(msg)
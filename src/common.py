import os

import src.config as config

class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}
    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]

def get_root_dir() -> str:
    """Return absolute path of project, client or server program
       is both suitable."""
    path = os.path.dirname(__file__)
    return path

def get_client_log_dir() -> str:
    """Return absolute path of client log directory."""
    path = os.path.join(get_root_dir(), config.CLI_LOG_DIR)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_client_log_file_path() -> str:
    """Return absolute path of client log file."""
    path = os.path.abspath(os.path.join(get_client_log_dir(),
                                        config.CLI_CLIENT_LOG))
    return path

def get_server_log_dir() -> str:
    """Return absolute path of server log directory."""
    path = os.path.join(get_root_dir(), config.SVR_LOG_DIR)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_server_rule_log_file_path() -> str:
    """Return absolute path of server rule log."""
    path = os.path.abspath(os.path.join(get_server_log_dir(),
                                        config.SVR_RULE_CHECK_LOG))
    return path

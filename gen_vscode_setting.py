import os
import sys
import json
sys.dont_write_bytecode = True # 不生成 .pyc 文件

import src.config as config


def gen_python_path():
    """生成 settings.json 文件中的自动补全和代码分析配置."""
    vscode_settings = None
    with open(r".vscode/settings.json", "r") as f:
        vscode_settings = json.load(f)

    paths = []
    paths.append(os.path.abspath(config.DATA_DIR))
    paths.append(os.path.abspath(os.getcwd()))
    # paths.append(os.path.abspath(os.path.join(os.getcwd(), "src")))

    vscode_settings["python.autoComplete.extraPaths"] = paths
    vscode_settings["python.analysis.extraPaths"] = paths

    with open(r".vscode/settings.json", "w") as f:
        json.dump(vscode_settings, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    gen_python_path()
# 配置检查器

# 要求

Python version >= Python3.5
install pyqt5 requests

## 配置使用环境

1. [必选]修改 `src/config.py`, 将 `SVR_DATA_DIR` 改为策划配置表目录.
2. [可选]执行 `gen_vscode.py`, 为 VSCode 开发环境生成 `settings.json` 文件中的自动补全和代码分析配置.


## 使用配置检查器

进入 `src/server/` 目录, 执行 `python server.py`, 启动配置检查服务器. 然后进入 `src/client/` 目录，执行 `python client.py`, 启动配置检查客户端.

## 客户端截图

![avatar](./pictures/client1.png)


## 开发新的配置检查项

如果是想对新的配置表进行检查, 步骤如下

在 `src/server/rules/` 目录下建立新的 Python 文件，命名按照 `modulename_rule.py`
的规则.

在文件内添加检测函数, 格式如下

```python
# 导入需要检查的配置表
import Some_Config_Table

# 检测函数必须使用 @RM.reg_check_rule() 装饰器
@RM.reg_check_rule()
def check_XXXX() -> bool:
    """检测函数说明.检测函数内部可以使用 debug_log, info_log, warn_log, error_log 四个日志打印函数.

    Args: 检测函数没有参数

    Returns: 检测函数返回一个 bool 值, True 表示检测成功, False 表示检测失败
    """
    flag = True
    # 具体的检测逻辑由开发者补充
    return flag
```

开发者只需要完成检测函数的编写即可，不用关心其他的任何逻辑.


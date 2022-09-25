import os
import sys
import logging
import functools
import json

import requests
from PyQt5.QtWidgets import (QMainWindow, QCheckBox, QGroupBox, QHBoxLayout,
                            QWidget, QVBoxLayout, QApplication, QTextEdit,
                            QPushButton, QLineEdit)
from PyQt5.QtGui import QFont, QColor, QTextCursor, QTextCharFormat, QIcon

root_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.append(root_dir)
import src.config as config


# define some colors
RED         = QColor(255,   0,   0)
ORANGE      = QColor(255,  69,   0)
BLUE        = QColor(  0,   0, 139)
GREEN       = QColor(  0, 205,   0)
DEEP_BLUE   = QColor(  0, 191, 255)
GOLD        = QColor(238, 201,   0)


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        # 数据定义
        self.rule_groups = ["全选"]
        self.text_log = []
        self.hl_words = [("error", RED), ("warn", ORANGE), ("info", GREEN)]
        self.hl_flag = True

        # UI 组件定义
        self.statusbar = None
        self.group_box = None
        self.left_btn_widget = QWidget()
        self.right_btn_widget = QWidget()
        self.check_boxs = []
        self.main_layout = None
        self.center_widget = QWidget()
        self.left_widget = QWidget()
        self.right_widget = QWidget()
        self.search_widget = QWidget()

        # 执行初始化流程
        self.init()


###########################################################
# 初始化逻辑
###########################################################

    def init(self):
        self._init_base_ui()
        self._svr_connect()
        self._init_ui()


###########################################################
# 客户端 UI
###########################################################

    def _init_base_ui(self):
        self.statusbar = self.statusBar()
        self.main_layout = QHBoxLayout()

    def _init_ui(self):
        # 左侧窗口
        left_layout = QVBoxLayout()
        self._init_group_box()
        left_layout.addWidget(self.group_box)
        left_layout.addStretch()
        self._init_left_button()
        left_layout.addWidget(self.left_btn_widget)

        self.left_widget.setLayout(left_layout)
        self.main_layout.addWidget(self.left_widget)
        self.main_layout.setStretchFactor(self.left_widget, 10)

        # 中间窗口
        self._init_text_edit()
        self.main_layout.addWidget(self.text_edit)
        self.main_layout.setStretchFactor(self.text_edit, 70)

        # 右侧窗口
        right_layout = QVBoxLayout()
        self._init_right_button()
        right_layout.addWidget(self.right_btn_widget)
        self._init_serch_widget()
        right_layout.addWidget(self.search_widget)
        right_layout.addStretch(10) # 让搜索框靠近上边

        self.right_widget.setLayout(right_layout)
        self.main_layout.addWidget(self.right_widget)
        self.main_layout.setStretchFactor(self.right_widget, 20)

        # 主窗口配置
        self.setWindowTitle("配置检查器")
        self.setWindowIcon(QIcon("./icon.png"))
        self.resize(1300, 800)
        self.center_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.center_widget)

    def _init_group_box(self):
        logging.info("_init_group_box")
        layout = QVBoxLayout()
        self.group_box = QGroupBox("配置表规则检查组")
        self.group_box.setFlat(True)

        for rule_group in self.rule_groups:
            check_box:QCheckBox = QCheckBox(rule_group)
            check_box.setChecked(False)
            check_box.stateChanged.connect(functools.partial(self._slot_checkbox, check_box))
            layout.addWidget(check_box)
            self.check_boxs.append(check_box)

        layout.addStretch() # keep check_boxs 让选项保持在一起，不要分隔的太远
        self.group_box.setLayout(layout)

    def _init_text_edit(self):
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self._slot_text_edit()

    def _init_left_button(self):
        layout = QVBoxLayout()
        self.exec_rule_btn:QPushButton = QPushButton("执行检查")
        self.clear_log_btn:QPushButton = QPushButton("清空日志")
        self.sync_log_btn:QPushButton  = QPushButton("同步日志")

        # "执行检查"按钮在没有规则被选中的时候不可点击
        self.exec_rule_btn.setEnabled(False)

        self.exec_rule_btn.clicked.connect(lambda: self._slot_exec_rule(self.exec_rule_btn))
        self.clear_log_btn.clicked.connect(lambda: self._slot_clear_log(self.clear_log_btn))
        self.sync_log_btn.clicked.connect(lambda: self._slot_sync_log(self.sync_log_btn))

        layout.addStretch() # 让按钮贴近下边沿
        layout.addWidget(self.exec_rule_btn)
        layout.addWidget(self.clear_log_btn)
        layout.addWidget(self.sync_log_btn)
        self.left_btn_widget.setLayout(layout)

    def _init_right_button(self):
        layout = QVBoxLayout()
        placeholder_widget = QWidget() # 占位
        layout.addStretch(20)
        layout.addWidget(placeholder_widget)
        layout.setStretchFactor(placeholder_widget, 50)

        btn_widget = QWidget()
        btn_layout = QVBoxLayout()


        self.font_add_btn:QPushButton = QPushButton("放大字体")
        self.font_sub_btn:QPushButton = QPushButton("缩小字体")
        self.text_lh_btn:QPushButton  = QPushButton("切换高亮")

        self.font_add_btn.clicked.connect(lambda: self._slot_font_add(self.font_add_btn))
        self.font_sub_btn.clicked.connect(lambda: self._slot_font_sub(self.font_sub_btn))
        self.text_lh_btn.clicked.connect(lambda: self._slot_text_hl(self.text_lh_btn))

        btn_layout.addWidget(self.font_add_btn)
        btn_layout.addWidget(self.font_sub_btn)
        btn_layout.addWidget(self.text_lh_btn)
        btn_layout.addStretch() # 让按钮贴近上边沿

        btn_widget.setLayout(btn_layout)
        layout.addWidget(btn_widget)
        layout.setStretchFactor(btn_widget, 50)
        self.right_btn_widget.setLayout(layout)

    def _init_serch_widget(self):
        layout = QHBoxLayout()
        self.search_line_edit:QLineEdit = QLineEdit()
        self.search_line_edit.setMaxLength(10)
        self.search_btn:QPushButton = QPushButton("过滤")
        self.search_btn.setEnabled(False)

        self.search_line_edit.textChanged.connect(lambda: self._slot_search_line_edit(self.search_line_edit))
        self.search_btn.clicked.connect(lambda: self._slot_search_btn(self.search_btn))

        layout.addWidget(self.search_line_edit)
        layout.addWidget(self.search_btn)
        layout.setStretchFactor(self.search_line_edit, 80)
        layout.setStretchFactor(self.search_btn, 20)

        self.search_widget.setLayout(layout)


###########################################################
# 客户端日志管理
###########################################################
    def _append_log(self, log:str):
        if not log:
            return
        if not log.endswith('\n'):
            log += '\n'
        self.text_log.append(log)

    def _clear_log(self):
        self.text_log.clear()

    def _get_log_str(self) -> str:
        return "".join(self.text_log)

###########################################################
# 信号槽
###########################################################

    def _slot_checkbox(self, check_box:QCheckBox):
        if check_box.text() == "全选":
            check_state = check_box.isChecked()
            for cb in self.check_boxs:
                cb.setChecked(check_state)

        have_rule_selected = False
        for cb in self.check_boxs:
            if cb.isChecked():
                have_rule_selected = True

        # 设置"执行检查"按钮可被点击
        self.exec_rule_btn.setEnabled(have_rule_selected)

    def _slot_exec_rule(self, btn:QPushButton):
        rules = []
        for cb in self.check_boxs:
            if cb.text() == "全选": continue # 过滤掉全选按钮
            if cb.isChecked():
                rules.append(cb.text())

        if not rules:
            msg = "[WARN] no rules was selected."
            self._append_log(msg)
            self._slot_text_edit()
            return

        msg = "[CLIENT] exec_rules: {}".format(rules)
        self._append_log(msg)

        self._svr_exec_rules(rules)
        self._slot_text_edit()


    def _slot_clear_log(self, btn:QPushButton):
        self._clear_log()
        self._slot_text_edit()

    def _slot_sync_log(self, btn:QPushButton):
        self._svr_sync_log()

    def _slot_text_edit(self, adj_font=0, adj_font_step=1, show_text=None, hl_word=None):
        if not show_text:
            show_text = self._get_log_str()
        # 填充文字
        self.text_edit.setPlainText(show_text)

        # 设置字体
        font:QFont = self.text_edit.font()
        if adj_font > 0:
            font.setPointSize(font.pointSize() + adj_font_step)
        elif adj_font < 0:
            font.setPointSize(font.pointSize() - adj_font_step)
        self.text_edit.setFont(font)

        # 设置关键字高亮
        doc = self.text_edit.document()
        cursor = QTextCursor(doc)
        cursor.beginEditBlock()
        if self.hl_flag:
            for (word, color) in self.hl_words:
                hl_cursor = QTextCursor(doc)
                color_fmt = QTextCharFormat(hl_cursor.charFormat())
                color_fmt.setForeground(color)
                while (not hl_cursor.isNull()) and (not hl_cursor.atEnd()):
                    hl_cursor = doc.find(word, hl_cursor)
                    if not hl_cursor.isNull():
                        hl_cursor.mergeCharFormat(color_fmt)
        # 搜索模式下高亮搜索的关键字
        if hl_word:
            hl_cursor = QTextCursor(doc)
            color_fmt = QTextCharFormat(hl_cursor.charFormat())
            color_fmt.setBackground(GOLD)
            while (not hl_cursor.isNull()) and (not hl_cursor.atEnd()):
                hl_cursor = doc.find(hl_word, hl_cursor)
                if not hl_cursor.isNull():
                    hl_cursor.mergeCharFormat(color_fmt)
        cursor.endEditBlock()
        # 重绘
        self.text_edit.setTextCursor(cursor)


    def _slot_font_add(self, btn:QPushButton):
        self._slot_text_edit(adj_font=1)

    def _slot_font_sub(self, btn:QPushButton):
        self._slot_text_edit(adj_font=-1)

    def _slot_text_hl(self, btn:QPushButton):
        self.hl_flag = not self.hl_flag
        self._slot_text_edit()

    def _slot_search_line_edit(self, line_edit:QLineEdit):
        btn_enable = line_edit.text() != ""
        self.search_btn.setEnabled(btn_enable)

    def _slot_search_btn(self, btn:QPushButton):
        word = self.search_line_edit.text()
        if not word:
            return
        fliter_log = [line for line in self.text_log if word in line]
        show_text = "".join(fliter_log)
        self._slot_text_edit(show_text=show_text, hl_word=word)

###########################################################
# 客户端/服务器交互逻辑
###########################################################

    def gen_url(self, params:str):
        url = "http://{}:{}/{}".format(config.CLI_SERVER_IP, config.CLI_SERVER_PORT, params)
        return url

    def _svr_connect(self):
        self.statusbar.showMessage("获取服务器配置...", 3000)
        # 获取服务器配置逻辑
        url = self.gen_url("req_rule_group")
        rsp = requests.get(url)
        data = json.loads(rsp.text)
        rule_groups = data.get("rule_groups")
        self.rule_groups.extend(rule_groups)
        self.statusbar.showMessage("获取服务器配置完成.", 3000)

    def _svr_exec_rules(self, rules:list) -> None:
        url = self.gen_url("check_rule")
        params = {"rule_groups": rules}
        rsp = requests.post(url, data=params)
        data = json.loads(rsp.text)
        for line in data.get("text_log").split("\n"):
            self._append_log(line)
        self._slot_text_edit()

    def _svr_sync_log(self) -> None:
        url = self.gen_url("sync_log")
        rsp = requests.get(url)
        data = json.loads(rsp.text)
        for line in data.get("total_log").split("\n"):
            self._append_log(line)
        self._slot_text_edit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWin()
    main_win.show()
    sys.exit(app.exec_())
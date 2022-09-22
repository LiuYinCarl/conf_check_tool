import sys
import os
import logging
import functools
from urllib.parse import quote_plus
from PyQt5.QtWidgets import (QMainWindow, QCheckBox, QGroupBox, QHBoxLayout,
    QWidget, QVBoxLayout, QApplication, QTextEdit, QPushButton)
from PyQt5.QtGui import QFont, QColor, QTextCursor, QTextCharFormat


RED =    QColor(255, 0, 0)
ORANGE = QColor(255, 69, 0)
BLUE =   QColor(0, 0, 139)


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        # 数据定义
        self.rule_groups = ["全选", "rule1", "rule2", "rule3"]
        self.text_log = "this is a error warn log info.\n"
        self.hl_words = [("error", RED), ("warn", ORANGE), ("log", BLUE)]
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

        # 中间窗口
        self._init_text_edit()
        self.main_layout.addWidget(self.text_edit)

        # 右侧窗口
        right_layout = QVBoxLayout()
        self._init_right_button()
        right_layout.addWidget(self.right_btn_widget)

        self.right_widget.setLayout(right_layout)
        self.main_layout.addWidget(self.right_widget)

        # 主窗口配置
        self.setWindowTitle("配置检查器")
        self.resize(1200, 800)
        self.center_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.center_widget)

    def _init_group_box(self):
        logging.info("_init_group_box")
        layout = QVBoxLayout()
        self.group_box = QGroupBox("配置表规则检查组")
        self.group_box.setFlat(True)

        for rule_group in self.rule_groups:
            check_box:QCheckBox = QCheckBox(rule_group)
            print(id(check_box))
            check_box.setChecked(False)
            # wrong method. but don't know why
            # check_box.stateChanged.connect(lambda cbs=check_box: self._slot_checkbox(cbs))
            check_box.stateChanged.connect(functools.partial(self._slot_checkbox, check_box))
            layout.addWidget(check_box)
            self.check_boxs.append(check_box)

        layout.addStretch() # keep check_boxs 让选项保持在一起，不要分隔的太远
        self.group_box.setLayout(layout)

    def _init_text_edit(self):
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        # self.text_edit.setPlainText(self.text_log)
        self._slot_text_edit()

    def _init_left_button(self):
        layout = QVBoxLayout()
        self.exec_rule_btn:QPushButton = QPushButton("执行检查")
        self.clear_log_btn:QPushButton = QPushButton("清空日志")
        self.sync_log_btn:QPushButton  = QPushButton("同步日志")

        self.exec_rule_btn.clicked.connect(lambda: self._slot_exec_rule(self.exec_rule_btn))
        self.clear_log_btn.clicked.connect(lambda: self._slot_clear_log(self.clear_log_btn))
        self.sync_log_btn.clicked.connect(lambda: self._slot_sync_log(self.sync_log_btn))

        layout.addStretch() # 让按钮贴近下边沿
        layout.addWidget(self.exec_rule_btn)
        layout.addWidget(self.clear_log_btn)
        layout.addWidget(self.sync_log_btn)
        self.left_btn_widget.setLayout(layout)

    def _init_right_button(self):
        print("_init_right_button")
        layout = QVBoxLayout()
        self.font_add_btn:QPushButton = QPushButton("放大字体")
        self.font_sub_btn:QPushButton = QPushButton("缩小字体")
        self.text_lh_btn:QPushButton  = QPushButton("切换高亮")

        self.font_add_btn.clicked.connect(lambda: self._slot_font_add(self.font_add_btn))
        self.font_sub_btn.clicked.connect(lambda: self._slot_font_sub(self.font_sub_btn))
        self.text_lh_btn.clicked.connect(lambda: self._slot_text_hl(self.text_lh_btn))

        layout.addWidget(self.font_add_btn)
        layout.addWidget(self.font_sub_btn)
        layout.addWidget(self.text_lh_btn)
        layout.addStretch() # 让按钮贴近上边沿
        self.right_btn_widget.setLayout(layout)


###########################################################
# 信号槽
###########################################################

    def _slot_checkbox(self, check_box:QCheckBox):
        msg = "_slot_checkbox id:{} state:{}".format(id(check_box), check_box.isChecked())
        print(msg)
        self.text_log += "{}\n".format(msg)

        if check_box.text() == "全选":
            check_state = check_box.isChecked()
            for cb in self.check_boxs:
                cb.setChecked(check_state)

        self._slot_text_edit()

    def _slot_exec_rule(self, btn:QPushButton):
        rules = []
        for cb in self.check_boxs:
            if cb.text() == "全选": continue # 过滤掉全选按钮
            if cb.isChecked():
                rules.append(cb.text())
        self._svr_exec_rules(rules)

        msg = "exec_rules: {}".format(rules)
        self.text_log += "{}\n".format(msg)
        self._slot_text_edit()


    def _slot_clear_log(self, btn:QPushButton):
        self.text_log = ""
        self._slot_text_edit()

    def _slot_sync_log(self, btn:QPushButton):
        self._svr_sync_log()

    def _slot_text_edit(self, adj_font=0, adj_font_step=1):
        # 填充文字
        self.text_edit.setPlainText(self.text_log)

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

###########################################################
# 客户端/服务器交互逻辑
###########################################################

    def _svr_connect(self):
        self.statusbar.showMessage("获取服务器配置...", 3000)
        # 获取服务器配置逻辑
        self.statusbar.showMessage("获取服务器配置完成.", 3000)

    def _svr_exec_rules(self, rules:list) -> None:
        pass

    def _svr_sync_log(self) -> None:
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWin()
    main_win.show()
    sys.exit(app.exec_())
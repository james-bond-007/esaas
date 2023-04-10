import sys
import random
from enum import Enum, unique
from typing import Type
from PySide6 import QtCore, QtWidgets, QtGui, QtMultimedia
from PySide6.QtCore import Qt
import operator
import pygame

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()

def play_audio_file(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
def play_audio_file_async(file_path):
    sound = pygame.mixer.Sound(file_path)
    sound.play()

class CalcType(str, Enum):
    Addition = "连加"
    Subtraction1 = "连减"
    AdditionSubtraction = "先加后减"
    SubtractionAddition = "先减后加"

class MyWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.select = CalcType.Addition
        self.result = 0
        self.setWindowTitle("20以内加减法")
        self.resize(400, 400)
        self.setup_ui()
        self.print_20_mix()
        self.label_C.setPixmap(QtGui.QPixmap("None.png"))
        self.correct_player =  QtMultimedia.QSoundEffect()
        self.correct_player.setSource(QtCore.QUrl.fromLocalFile("correct.wav"))
        self.correct_player.setLoopCount(1)
        self.correct_player.setVolume(1.0)
        self.incorrect_player = QtMultimedia.QSoundEffect()
        self.incorrect_player.setSource(QtCore.QUrl.fromLocalFile("incorrect.wav"))
        self.incorrect_player.setLoopCount(1)
        self.incorrect_player.setVolume(1.0)
    def print_calc(self, a: int, b: int, c: int, operator1: str, operator2: str) -> str:
        valid_operators = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
        if operator1 not in valid_operators or operator2 not in valid_operators:
            raise ValueError(f"Invalid operator name: {operator1} or {operator2}")
        op_func1 = valid_operators[operator1]
        op_func2 = valid_operators[operator2]
        self.result = op_func2(op_func1(a, b), c)
        return f"{a} {operator1} {b} {operator2} {c} ="

    def print_10(self):
        for _ in range(1000):
            a = random.randint(3, 10)
            b = random.randint(1, a)
            print(f"{a} - {b} = ")

    def print_20(self):
        for _ in range(1020):
            a = random.randint(10, 20)
            b = random.randint(1, a)
            print(f"{a} - {b} = ")

    def print_20b(self):
        for _ in range(1020):
            a = random.randint(10, 20)
            b = random.randint(1, 10)
            print(f"{a} - {b} = ")

    def print_20_mix(self):
        calc_typ = self.select
        if calc_typ == CalcType.Addition:
            a = random.randint(1, 18)
            b = random.randint(1, 19 - a)
            c = random.randint(1, 20 - a - b)
            gs = self.print_calc(a, b, c, "+", "+")
        elif calc_typ == CalcType.Subtraction1:
            a = random.randint(10, 20)
            b = random.randint(1, a - 2)
            c = random.randint(1, a - b - 1)
            gs = self.print_calc(a, b, c, "-", "-")
        elif calc_typ == CalcType.AdditionSubtraction:
            a = random.randint(1, 19)
            b = random.randint(1, 20 - a)
            c = random.randint(1, a + b)
            gs = self.print_calc(a, b, c, "+", "-")
        elif calc_typ == CalcType.SubtractionAddition:
            a = random.randint(10, 20)
            b = random.randint(1, a - 1)
            c = random.randint(1, 20 - (a - b))
            gs = self.print_calc(a, b, c, "-", "+")
        self.label_A.setText(gs)

    def d_result(self):
        try:
            if self.result == int(self.line_edit.text()):
                self.label_B.setStyleSheet("color:green;")
                self.label_B.setText("✓")
                self.label_C.setPixmap(QtGui.QPixmap("laught.png"))
                # self.correct_player.play()
                play_audio_file_async("correct.wav")
            else:
                self.label_B.setStyleSheet("color:red;")
                self.label_B.setText("✗")
                self.label_C.setPixmap(QtGui.QPixmap("cry.png"))
                # self.incorrect_player.play()
                play_audio_file_async("incorrect.wav")
        except ValueError:
            message_box = QtWidgets.QMessageBox()
            message_box.setText("请输入数字！")
            message_box.exec_()

    def d_generate(self):
        self.print_20_mix()
        self.line_edit.setText("")
        self.label_B.setText("    ")
        self.label_C.setPixmap(QtGui.QPixmap("None.png"))

    def setup_ui(self) -> None:
        """设置界面"""
        # 题目类型
        self.type_groupbox = QtWidgets.QGroupBox("类型")
        self.type_groupbox.setFont(QtGui.QFont("Helvetica", 16, QtGui.QFont.Bold))
        # self.type_groupbox.setTitle("<font color='blue'>题目类型22</font>")
        self.type_groupbox.setStyleSheet("font-size: 16px;")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor("blue"))
        self.type_groupbox.setPalette(palette)

        self.radio_buttons = []
        for index, name in CalcType.__members__.items():
            button = QtWidgets.QRadioButton(name.value)
            button.setFont(QtGui.QFont("Helvetica", 16, QtGui.QFont.Bold))
            button.clicked.connect(self.update_preview)
            self.radio_buttons.append(button)

        layout = QtWidgets.QHBoxLayout()
        for button in self.radio_buttons:
            layout.addWidget(button)
        self.radio_buttons[0].setChecked(True)
        self.type_groupbox.setLayout(layout)

        # 题目
        self.other_groupbox = QtWidgets.QGroupBox("题目")
        self.other_groupbox.setFont(QtGui.QFont("Helvetica", 16, QtGui.QFont.Bold))
        self.other_groupbox.setStyleSheet("font-size: 16px;")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor("blue"))
        self.other_groupbox.setPalette(palette)

        self.label_A = QtWidgets.QLabel(self)
        self.label_A.setFont(QtGui.QFont("Times New Roman", 25, QtGui.QFont.Bold))
        self.label_A.setText("                   ")
        self.label_A.setStyleSheet("font-size: 25px;")

        self.label_B = QtWidgets.QLabel(self)
        self.label_B.setFont(QtGui.QFont("Times New Roman", 25, QtGui.QFont.Bold))
        self.label_B.setText("    ")
        self.label_B.setStyleSheet("font-size: 25px;")

        self.label_C = QtWidgets.QLabel(self)
        self.label_C.setStyleSheet("font-size: 25px;")

        self.line_edit = QtWidgets.QLineEdit(self)
        self.line_edit.setFont(QtGui.QFont("Times New Roman", 25, QtGui.QFont.Bold))
        self.line_edit.setPlaceholderText("结果")
        self.line_edit.setStyleSheet("font-size: 25px;")

        self.generate_button = QtWidgets.QPushButton("生成")
        self.generate_button.setFont(QtGui.QFont("Helvetica", 16))
        self.generate_button.clicked.connect(self.d_generate)

        self.verify_button = QtWidgets.QPushButton("验证")
        self.verify_button.setFont(QtGui.QFont("Helvetica", 16))
        self.verify_button.clicked.connect(self.d_result)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.label_A)
        h_layout.addWidget(self.line_edit)
        h_layout.addWidget(self.label_B)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(h_layout)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.verify_button)
        layout.addWidget(self.label_C, alignment=Qt.AlignCenter)

        self.other_groupbox.setLayout(layout)

        # 整个界面
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.type_groupbox)
        main_layout.addWidget(self.other_groupbox)
        self.setLayout(main_layout)

    def update_preview(self) -> None:
        """
        更新预览窗口的题目类型
        """
        for button in self.radio_buttons:
            if button.isChecked():
                self.select = button.text()
                break
        self.d_generate()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        窗口关闭事件，弹出对话框提示用户是否退出程序
        """
        result = QtWidgets.QMessageBox.question(
            self,
            "关闭程序",
            "你确定要退出吗？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if result == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QPlainTextEdit

from ctypes import windll

from app_database.database_methods import get_app_id, get_user_data_from_app_database, write_log, app_style

from cloud_database.spreadsheets_methods import write_bug_report


class BugReportWindow(QMainWindow):
    def __init__(self) -> None:
        try:
            super().__init__()

            windll.shell32.SetCurrentProcessExplicitAppUserModelID(get_app_id())

            self.setWindowTitle('Отправка отчета об ошибке - CrocodileReader')
            self.setFixedSize(400, 400)
            self.move(0, 0)
            self.setWindowIcon(QIcon('../assets/app_icon.png'))
            self.setStyleSheet(app_style())

            self.txt_question_1 = QLabel('Какая ошибка возникла?', self)
            self.txt_question_1.resize(200, 20)
            self.txt_question_1.move(100, 10)

            self.input_question_1 = QPlainTextEdit('', self)
            self.input_question_1.resize(200, 50)
            self.input_question_1.move(100, 40)

            self.txt_question_2 = QLabel('Подробно опишите, какие действия\nпривели к ошибке:', self)
            self.txt_question_2.resize(200, 40)
            self.txt_question_2.move(100, 100)

            self.input_question_2 = QPlainTextEdit('', self)
            self.input_question_2.resize(200, 50)
            self.input_question_2.move(100, 150)

            self.txt_question_3 = QLabel('Укажите контактный e-mail', self)
            self.txt_question_3.resize(200, 20)
            self.txt_question_3.move(100, 210)

            self.input_question_3 = QPlainTextEdit(get_user_data_from_app_database('email'), self)
            self.input_question_3.resize(200, 50)
            self.input_question_3.move(100, 240)

            self.txt_message = QLabel('Логи отправятся после нажатия\nкнопки "Отправить"', self)
            self.txt_message.resize(200, 40)
            self.txt_message.move(100, 300)

            self.btn = QPushButton('Отправить отчет', self)
            self.btn.resize(200, 40)
            self.btn.move(100, 350)
            self.btn.clicked.connect(self.send)
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def send(self) -> None:
        try:
            write_bug_report(self.input_question_1.toPlainText(), self.input_question_2.toPlainText(),
                             self.input_question_3.toPlainText())
            self.close()
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

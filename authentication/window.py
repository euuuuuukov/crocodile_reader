from PyQt6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel
from PyQt6.QtGui import QIcon, QResizeEvent
from PyQt6.QtCore import QSize

from ctypes import windll

from app_database.database_methods import get_app_id, rewrite_authentication

from authentication.compliance_authentication import compliance_get_code, compliance_sign_up

from email_sending.email_methods import send_authentication_email

from cloud_database.spreadsheets_methods import do_authentication, do_sign_in

from bug_report.window import BugReport

from main_window.window import MainWindow


class AuthWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        windll.shell32.SetCurrentProcessExplicitAppUserModelID(get_app_id())

        with open('../interface/error_authentication_style.txt', 'r', encoding='utf-8') as error_authentication_style:
            self.style_text_error = error_authentication_style.read()

        self.setMinimumSize(400, 400)
        self.move(0, 0)
        self.setWindowIcon(QIcon('../assets/app_icon.png'))

        self.btn_choose_sign_in = QPushButton('Вход', self)
        self.btn_choose_sign_in.clicked.connect(self.sign_in)

        self.btn_choose_sign_up = QPushButton('Регистрация', self)
        self.btn_choose_sign_up.clicked.connect(self.sign_up)

        self.input_sign_in_email = QLineEdit('', self)
        self.input_sign_in_email.setPlaceholderText('E-mail')

        self.input_sign_in_password = QLineEdit('', self)
        self.input_sign_in_password.setPlaceholderText('Пароль')

        self.text_error_sign_in = QLabel('', self)
        self.text_error_sign_in.setStyleSheet(self.style_text_error)

        self.btn_sign_in_see_password = QPushButton('', self)
        self.btn_sign_in_see_password.setIcon(QIcon('../assets/show_password.png'))
        self.btn_sign_in_see_password_is_hided = True
        self.btn_sign_in_see_password.clicked.connect(self.sign_in_see_password)

        self.btn_sign_in = QPushButton('Войти!', self)
        self.btn_sign_in.clicked.connect(self.end_sign_in)

        self.input_sign_up_name = QLineEdit('', self)
        self.input_sign_up_name.setPlaceholderText('Имя')

        self.input_sign_up_surname = QLineEdit('', self)
        self.input_sign_up_surname.setPlaceholderText('Фамилия')

        self.text_error_name = QLabel('', self)
        self.text_error_name.setStyleSheet(self.style_text_error)

        self.input_sign_up_email = QLineEdit('', self)
        self.input_sign_up_email.setPlaceholderText('E-mail')

        self.text_error_email = QLabel('', self)
        self.text_error_email.setStyleSheet(self.style_text_error)

        self.btn_sign_up_code = QPushButton('Получить код', self)
        self.btn_sign_up_code.clicked.connect(self.get_code)

        self.input_sign_up_code = QLineEdit('', self)
        self.input_sign_up_code.setPlaceholderText('Код подтверждения')

        self.text_error_code = QLabel('', self)
        self.text_error_code.setStyleSheet(self.style_text_error)

        self.input_sign_up_password = QLineEdit('', self)
        self.input_sign_up_password.setEchoMode(QLineEdit().EchoMode.Password)
        self.input_sign_up_password.setPlaceholderText('Пароль')

        self.input_sign_up_repeat_password = QLineEdit('', self)
        self.input_sign_up_repeat_password.setEchoMode(QLineEdit().EchoMode.Password)
        self.input_sign_up_repeat_password.setPlaceholderText('Повторите пароль')

        self.btn_sign_up_see_password = QPushButton('', self)
        self.btn_sign_up_see_password.setIcon(QIcon('../assets/show_password.png'))
        self.btn_sign_up_see_password_is_hided = True
        self.btn_sign_up_see_password.clicked.connect(self.sign_up_see_password)

        self.text_error_password = QLabel('', self)
        self.text_error_password.setStyleSheet(self.style_text_error)

        self.btn_sign_up = QPushButton('Зарегистрироваться!', self)
        self.btn_sign_up.clicked.connect(self.end_sign_up)

        self.btn_bug_report = QPushButton('Отправить отчет об ошибке', self)
        self.btn_bug_report.clicked.connect(self.bug_report)

        self.bug_report_window = BugReport()
        self.bug_report_window.close()

        self.main_window = MainWindow([0, 0, 400, 400])
        self.main_window.close()

        self.show()

        self.sign_in()

    def sign_in(self) -> None:
        self.setWindowTitle('Вход - CrocodileReader')

        self.input_sign_in_email.show()
        self.input_sign_in_password.show()
        self.text_error_sign_in.show()
        self.btn_sign_in_see_password.show()
        self.btn_sign_in.show()

        self.input_sign_up_name.hide()
        self.input_sign_up_surname.hide()
        self.text_error_name.hide()
        self.input_sign_up_email.hide()
        self.text_error_email.hide()
        self.btn_sign_up_code.hide()
        self.input_sign_up_code.hide()
        self.text_error_code.hide()
        self.input_sign_up_password.hide()
        self.input_sign_up_repeat_password.hide()
        self.btn_sign_up_see_password.hide()
        self.text_error_password.hide()
        self.btn_sign_up.hide()

        self.btn_sign_in_see_password_is_hided = False
        self.sign_in_see_password()

    def sign_up(self) -> None:
        self.setWindowTitle('Регистрация - CrocodileReader')

        self.input_sign_in_email.hide()
        self.input_sign_in_password.hide()
        self.text_error_sign_in.hide()
        self.btn_sign_in_see_password.hide()
        self.btn_sign_in.hide()

        self.input_sign_up_name.show()
        self.input_sign_up_surname.show()
        self.text_error_name.show()
        self.input_sign_up_email.show()
        self.text_error_email.show()
        self.btn_sign_up_code.show()
        self.input_sign_up_code.show()
        self.text_error_code.show()
        self.input_sign_up_password.show()
        self.input_sign_up_repeat_password.show()
        self.btn_sign_up_see_password.show()
        self.text_error_password.show()
        self.btn_sign_up.show()

        self.btn_sign_up_see_password_is_hided = False
        self.sign_up_see_password()

    def sign_in_see_password(self) -> None:
        if self.btn_sign_in_see_password_is_hided:
            self.btn_sign_in_see_password_is_hided = False
            self.btn_sign_in_see_password.setIcon(QIcon('../assets/hide_password.png'))

            self.input_sign_in_password.setEchoMode(QLineEdit().EchoMode.Normal)
        else:
            self.btn_sign_in_see_password_is_hided = True
            self.btn_sign_in_see_password.setIcon(QIcon('../assets/show_password.png'))

            self.input_sign_in_password.setEchoMode(QLineEdit().EchoMode.Password)

    def sign_up_see_password(self) -> None:
        if self.btn_sign_up_see_password_is_hided:
            self.btn_sign_up_see_password_is_hided = False
            self.btn_sign_up_see_password.setIcon(QIcon('../assets/hide_password.png'))

            self.input_sign_up_password.setEchoMode(QLineEdit().EchoMode.Normal)
            self.input_sign_up_repeat_password.setEchoMode(QLineEdit().EchoMode.Normal)
        else:
            self.btn_sign_up_see_password_is_hided = True
            self.btn_sign_up_see_password.setIcon(QIcon('../assets/show_password.png'))

            self.input_sign_up_password.setEchoMode(QLineEdit().EchoMode.Password)
            self.input_sign_up_repeat_password.setEchoMode(QLineEdit().EchoMode.Password)

    def end_sign_in(self) -> None:
        email, password = self.input_sign_in_email.text(), self.input_sign_in_password.text()
        result = do_sign_in(email, password)
        if result.isdigit():
            rewrite_authentication(result)
            self.open_main_window()
        else:
            self.text_error_sign_in.setText(result)

    def get_code(self) -> None:
        name, surname = self.input_sign_up_name.text(), self.input_sign_up_surname.text()
        email = self.input_sign_up_email.text()
        result = compliance_get_code(name, surname, email)
        self.text_error_name.setText(result[0])
        self.text_error_email.setText(result[1])
        if result == ['', '']:
            self.text_error_code.setText(send_authentication_email(email, name, surname))

    def end_sign_up(self) -> None:
        name, surname = self.input_sign_up_name.text(), self.input_sign_up_surname.text()
        email, code = self.input_sign_up_email.text(), self.input_sign_up_code.text()
        password, repeat_password = self.input_sign_up_password.text(), self.input_sign_up_repeat_password.text()
        result = compliance_sign_up(name, surname, email, code, password, repeat_password)
        self.text_error_name.setText(result[0])
        self.text_error_email.setText(result[1])
        self.text_error_code.setText(result[2])
        self.text_error_password.setText(result[3])
        if result == ['', '', '', '']:
            rewrite_authentication(do_authentication(name, surname, email, password))
            self.open_main_window()

    def bug_report(self) -> None:
        self.bug_report_window = BugReport()
        self.bug_report_window.show()

    def open_main_window(self) -> None:
        self.main_window = MainWindow(self.geometry().getRect())
        self.main_window.show()
        self.close()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.btn_choose_sign_in.resize(self.width() // 3, self.height() // 12)
        self.btn_choose_sign_in.move(self.width() // 2 - self.width() // 3, self.height() // 20)

        self.btn_choose_sign_up.resize(self.width() // 3, self.height() // 12)
        self.btn_choose_sign_up.move(self.width() // 2, self.height() // 20)

        self.input_sign_in_email.resize(self.width() // 3 * 2, self.height() // 12)
        self.input_sign_in_email.move(self.width() // 2 - self.width() // 3, self.height() // 12 * 4)

        self.input_sign_in_password.resize(self.width() // 3 * 2 - self.height() // 12, self.height() // 12)
        self.input_sign_in_password.move(self.width() // 2 - self.width() // 3,
                                         self.height() // 12 * 5 + self.height() // 20)

        self.btn_sign_in_see_password.resize(self.height() // 12, self.height() // 12)
        self.btn_sign_in_see_password.move(self.width() // 2 + self.width() // 3 - self.height() // 12,
                                           self.height() // 12 * 5 + self.height() // 20)
        self.btn_sign_in_see_password.setIconSize(QSize(self.height() // 12 // 2, self.height() // 12 // 2))

        self.text_error_sign_in.resize(self.width() // 3 * 2, self.height() // 20)
        self.text_error_sign_in.move(self.width() // 2 - self.width() // 3,
                                     self.height() // 12 * 7 + self.height() // 20 * 2)

        self.btn_sign_in.resize(self.width() // 3 * 2, self.height() // 12)
        self.btn_sign_in.move(self.width() // 2 - self.width() // 3, self.height() // 12 * 7 + self.height() // 20 * 4)

        self.input_sign_up_name.resize(self.width() // 3, self.height() // 12)
        self.input_sign_up_name.move(self.width() // 2 - self.width() // 3, self.height() // 12 * 2)

        self.input_sign_up_surname.resize(self.width() // 3, self.height() // 12)
        self.input_sign_up_surname.move(self.width() // 2, self.height() // 12 * 2)

        self.text_error_name.resize(self.width() // 3 * 2, self.height() // 20)
        self.text_error_name.move(self.width() // 2 - self.width() // 3, self.height() // 12 * 3)

        self.input_sign_up_email.resize(self.width() // 3 * 2, self.height() // 12)
        self.input_sign_up_email.move(self.width() // 2 - self.width() // 3,
                                      self.height() // 12 * 3 + self.height() // 20)

        self.text_error_email.resize(self.width() // 3 * 2, self.height() // 20)
        self.text_error_email.move(self.width() // 2 - self.width() // 3, self.height() // 12 * 4 + self.height() // 20)

        self.btn_sign_up_code.resize(self.width() // 3, self.height() // 12)
        self.btn_sign_up_code.move(self.width() // 2 - self.width() // 3,
                                   self.height() // 12 * 4 + self.height() // 20 * 2)

        self.input_sign_up_code.resize(self.width() // 3, self.height() // 12)
        self.input_sign_up_code.move(self.width() // 2, self.height() // 12 * 4 + self.height() // 20 * 2)

        self.text_error_code.resize(self.width() // 3 * 2, self.height() // 20)
        self.text_error_code.move(self.width() // 2 - self.width() // 3,
                                  self.height() // 12 * 5 + self.height() // 20 * 2)

        self.input_sign_up_password.resize(self.width() // 3 * 2 - self.height() // 12 * 2, self.height() // 12)
        self.input_sign_up_password.move(self.width() // 2 - self.width() // 3,
                                         self.height() // 12 * 5 + self.height() // 20 * 3)

        self.input_sign_up_repeat_password.resize(self.width() // 3 * 2 - self.height() // 12 * 2, self.height() // 12)
        self.input_sign_up_repeat_password.move(self.width() // 2 - self.width() // 3,
                                                self.height() // 12 * 6 + self.height() // 20 * 3)

        self.btn_sign_up_see_password.resize(self.height() // 12 * 2, self.height() // 12 * 2)
        self.btn_sign_up_see_password.move(self.width() // 2 + self.width() // 3 - self.height() // 12 * 2,
                                           self.height() // 12 * 5 + self.height() // 20 * 3)
        self.btn_sign_up_see_password.setIconSize(QSize(self.height() // 12, self.height() // 12))

        self.text_error_password.resize(self.width() // 3 * 2, self.height() // 20)
        self.text_error_password.move(self.width() // 2 - self.width() // 3,
                                      self.height() // 12 * 7 + self.height() // 20 * 3)

        self.btn_sign_up.resize(self.width() // 3 * 2, self.height() // 12)
        self.btn_sign_up.move(self.width() // 2 - self.width() // 3, self.height() // 12 * 7 + self.height() // 20 * 4)

        self.btn_bug_report.resize(self.width() // 2.4, self.height() // 12)
        self.btn_bug_report.move(self.width() - self.width() // 2.4, self.height() - self.height() // 12)

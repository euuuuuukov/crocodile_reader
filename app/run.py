from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QPainter, QColor, QIcon, QResizeEvent
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton, QSlider, QPlainTextEdit, QCheckBox
from ctypes import windll


from sys import argv


class CrocodileReader(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.app_id = 'crocodile_reader.1.0'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.app_id)

        self.btn_choose_sign_in = QPushButton('Вход', self)
        self.btn_choose_sign_in.clicked.connect(self.sign_in)

        self.btn_choose_sign_up = QPushButton('Регистрация', self)
        self.btn_choose_sign_up.clicked.connect(self.sign_up)

        self.input_sign_in_login = QLineEdit('', self)
        self.input_sign_in_login.setPlaceholderText('Логин')

        self.input_sign_in_password = QLineEdit('', self)
        self.input_sign_in_password.setPlaceholderText('Пароль')

        self.btn_sign_in_see_password = QPushButton('', self)
        self.btn_sign_in_see_password.setIcon(QIcon('../assets/show_password.png'))
        self.btn_sign_in_see_password_is_hided = True
        self.btn_sign_in_see_password.clicked.connect(self.sign_in_see_password)

        self.btn_sign_in = QPushButton('Войти!', self)

        self.input_sign_up_name = QLineEdit('', self)
        self.input_sign_up_name.setPlaceholderText('Имя')

        self.input_sign_up_surname = QLineEdit('', self)
        self.input_sign_up_surname.setPlaceholderText('Фамилия')

        self.input_sign_up_email = QLineEdit('', self)
        self.input_sign_up_email.setPlaceholderText('E-mail')

        self.btn_sign_up_code = QPushButton('Получить код', self)

        self.input_sign_up_code = QLineEdit('', self)
        self.input_sign_up_code.setPlaceholderText('Код подтверждения')

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

        self.btn_sign_up = QPushButton('Зарегистрироваться!', self)

        self.init_ui()

    def sign_in(self) -> None:
        self.input_sign_in_login.show()
        self.input_sign_in_password.show()
        self.btn_sign_in.show()
        self.btn_sign_in_see_password.show()

        self.input_sign_up_name.hide()
        self.input_sign_up_surname.hide()
        self.input_sign_up_email.hide()
        self.btn_sign_up_code.hide()
        self.input_sign_up_code.hide()
        self.input_sign_up_password.hide()
        self.input_sign_up_repeat_password.hide()
        self.btn_sign_up_see_password.hide()
        self.btn_sign_up.hide()

        self.btn_sign_in_see_password_is_hided = False
        self.sign_in_see_password()

    def sign_up(self) -> None:
        self.input_sign_in_login.hide()
        self.input_sign_in_password.hide()
        self.btn_sign_in.hide()
        self.btn_sign_in_see_password.hide()

        self.input_sign_up_name.show()
        self.input_sign_up_surname.show()
        self.input_sign_up_email.show()
        self.btn_sign_up_code.show()
        self.input_sign_up_code.show()
        self.input_sign_up_password.show()
        self.input_sign_up_repeat_password.show()
        self.btn_sign_up_see_password.show()
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

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.btn_choose_sign_in.resize(self.width() // 3, self.height() // 12)
        self.btn_choose_sign_in.move(self.width() // 2 - self.width() // 3, self.height() // 20)

        self.btn_choose_sign_up.resize(self.width() // 3, self.height() // 12)
        self.btn_choose_sign_up.move(self.width() // 2, self.height() // 20)

        self.input_sign_in_login.resize(self.width() // 3 * 2, self.height() // 12)
        self.input_sign_in_login.move(self.width() // 2 - self.width() // 3, self.height() // 12 * 4)

        self.input_sign_in_password.resize(self.width() // 3 * 2 - self.height() // 12, self.height() // 12)
        self.input_sign_in_password.move(self.width() // 2 - self.width() // 3,
                                         self.height() // 12 * 5 + self.height() // 20)

        self.btn_sign_in_see_password.resize(self.height() // 12, self.height() // 12)
        self.btn_sign_in_see_password.move(self.width() // 2 + self.width() // 3 - self.height() // 12,
                                           self.height() // 12 * 5 + self.height() // 20)
        self.btn_sign_in_see_password.setIconSize(QSize(self.height() // 12 // 2, self.height() // 12 // 2))

        self.btn_sign_in.resize(self.width() // 3 * 2, self.height() // 12)
        self.btn_sign_in.move(self.width() // 2 - self.width() // 3, self.height() // 12 * 7 + self.height() // 20 * 4)

        self.input_sign_up_name.resize(self.width() // 3, self.height() // 12)
        self.input_sign_up_name.move(self.width() // 2 - self.width() // 3, self.height() // 12 * 2)

        self.input_sign_up_surname.resize(self.width() // 3, self.height() // 12)
        self.input_sign_up_surname.move(self.width() // 2, self.height() // 12 * 2)

        self.input_sign_up_email.resize(self.width() // 3 * 2, self.height() // 12)
        self.input_sign_up_email.move(self.width() // 2 - self.width() // 3,
                                      self.height() // 12 * 3 + self.height() // 20)

        self.btn_sign_up_code.resize(self.width() // 3, self.height() // 12)
        self.btn_sign_up_code.move(self.width() // 2 - self.width() // 3,
                                   self.height() // 12 * 4 + self.height() // 20 * 2)

        self.input_sign_up_code.resize(self.width() // 3, self.height() // 12)
        self.input_sign_up_code.move(self.width() // 2, self.height() // 12 * 4 + self.height() // 20 * 2)

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

        self.btn_sign_up.resize(self.width() // 3 * 2, self.height() // 12)
        self.btn_sign_up.move(self.width() // 2 - self.width() // 3, self.height() // 12 * 7 + self.height() // 20 * 4)

    def init_ui(self) -> None:
        self.setWindowTitle('CrocodileReader')
        self.setMinimumSize(400, 400)
        self.move(0, 0)
        self.setWindowIcon(QIcon('../assets/app_icon.png'))
        self.run_app()

    def run_app(self) -> None:
        with open('../database/is_authenticated.txt', 'r', encoding='utf-8') as is_authenticated:
            if is_authenticated.read() == '0':
                self.authentication_window()

    def authentication_window(self) -> None:
        self.btn_choose_sign_in.show()
        self.btn_choose_sign_up.show()

        self.sign_in()


app = QApplication(argv)
app.setWindowIcon(QIcon('../assets/app_icon.png'))
crocodile_reader = CrocodileReader()
crocodile_reader.show()
app.exec()

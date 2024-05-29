from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QColorDialog

from ctypes import windll

from app_database.database_methods import (get_app_id, get_user_data_from_app_database, rewrite_authentication,
                                           write_log, active_button_style, inactive_button_style, app_style,
                                           change_color)

from cloud_database.spreadsheets_methods import rewrite_user_info


class SettingsWindow(QMainWindow):
    def __init__(self) -> None:
        try:
            super().__init__()

            windll.shell32.SetCurrentProcessExplicitAppUserModelID(get_app_id())

            self.setWindowTitle('Настройки - CrocodileReader')
            self.setFixedSize(400, 400)
            self.move(0, 0)
            self.setWindowIcon(QIcon('../assets/app_icon.png'))
            self.setStyleSheet(app_style())

            self.btn_account = QPushButton('Аккаунт', self)
            self.btn_account.resize(100, 40)
            self.btn_account.move(10, 10)
            self.btn_account.clicked.connect(self.to_account)

            self.texts_account = [QLabel('ID\nпользователя', self), QLabel('Имя', self), QLabel('Фамилия', self),
                                  QLabel('E-mail', self), QLabel('Пароль', self)]
            self.line_edits_account = [QLineEdit(self) for _ in range(5)]
            data_types = ['id', 'name', 'surname', 'email', 'password']
            for i in range(5):
                self.line_edits_account[i].setText(get_user_data_from_app_database(data_types[i]))
                self.texts_account[i].resize(50, 40)
                self.texts_account[i].move(150, 10 + 50 * i)
                self.line_edits_account[i].resize(150, 40)
                self.line_edits_account[i].move(220, 10 + 50 * i)
            self.line_edits_account[0].setReadOnly(True)
            self.line_edits_account[3].setReadOnly(True)
            self.line_edits_account[4].setEchoMode(QLineEdit().EchoMode.Password)

            self.btn_save = QPushButton('Сохранить изменения', self)
            self.btn_save.resize(200, 40)
            self.btn_save.move(150, 300)
            self.btn_save.clicked.connect(self.save_changes)

            self.btn_color = QPushButton('Цвет', self)
            self.btn_color.resize(100, 40)
            self.btn_color.move(10, 60)
            self.btn_color.clicked.connect(self.to_color)

            self.color_buttons = [QPushButton('Цвет приложения', self), QPushButton('Цвет фона\nтекстовых полей', self),
                                  QPushButton('Цвет кнопок', self), QPushButton('Цвет панели\nменю', self),
                                  QPushButton('Цвет панели\nинструментов', self)]
            for btn_number in range(len(self.color_buttons)):
                self.color_buttons[btn_number].resize(200, 40)
                self.color_buttons[btn_number].move(150, 10 + 50 * btn_number)
                self.color_buttons[btn_number].clicked.connect(self.color)

            self.txt_color = QLabel('После изменения настроек\nнеобходимо перезапустить\nприложение', self)
            self.txt_color.resize(200, 70)
            self.txt_color.move(150, 300)

            self.to_account()
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def to_account(self) -> None:
        try:
            self.btn_account.setStyleSheet(active_button_style())
            self.btn_color.setStyleSheet(inactive_button_style())

            for label in self.texts_account:
                label.show()
            for line_edit in self.line_edits_account:
                line_edit.show()
            self.btn_save.show()

            for button in self.color_buttons:
                button.hide()
            self.txt_color.hide()
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def save_changes(self) -> None:
        index = self.line_edits_account[0].text()
        rewrite_user_info(index, self.line_edits_account[1].text(), self.line_edits_account[2].text(),
                          self.line_edits_account[4].text())
        rewrite_authentication(index)

    def to_color(self) -> None:
        try:
            self.btn_account.setStyleSheet(inactive_button_style())
            self.btn_color.setStyleSheet(active_button_style())

            for label in self.texts_account:
                label.hide()
            for line_edit in self.line_edits_account:
                line_edit.hide()
            self.btn_save.hide()

            for button in self.color_buttons:
                button.show()
            self.txt_color.show()
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def color(self) -> None:
        try:
            color = QColorDialog.getColor(QColor(0, 255, 0), self, 'Окно выбора цвета - CrocodileReader')
            if color.isValid():
                colors = [color.red(), color.green(), color.blue()]
                btn_txt = self.sender().text()
                if self.color_buttons[0].text() == btn_txt:
                    change_color(['QWidget'], colors)
                elif self.color_buttons[1].text() == btn_txt:
                    change_color(['QLineEdit', 'QTextEdit', 'QPlainTextEdit'], colors)
                elif self.color_buttons[2].text() == btn_txt:
                    change_color(['QPushButton'], colors)
                elif self.color_buttons[3].text() == btn_txt:
                    change_color(['QMenuBar'], colors)
                elif self.color_buttons[4].text() == btn_txt:
                    change_color(['QToolBar'], colors)
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

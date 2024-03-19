from PyQt6.QtGui import QIcon, QResizeEvent
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel

from ctypes import windll

from app_database.database_methods import get_app_id


class MainWindow(QMainWindow):
    def __init__(self, size: list[int]) -> None:
        super().__init__()

        windll.shell32.SetCurrentProcessExplicitAppUserModelID(get_app_id())

        self.setMinimumSize(400, 400)
        self.setGeometry(*size)
        self.setWindowIcon(QIcon('../assets/app_icon.png'))

        self.main_func()

    def main_func(self) -> None:
        self.setWindowTitle('Главная - CrocodileReader')

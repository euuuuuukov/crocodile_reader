from PyQt6.QtWidgets import QApplication

from sys import argv

from app_database.database_methods import is_authenticated

from authentication.window import AuthWindow

from main_window.window import MainWindow


def run_app() -> None:
    app = QApplication(argv)
    if not is_authenticated():
        crocodile_reader = AuthWindow()
        crocodile_reader.show()
    else:
        crocodile_reader = MainWindow([0, 0, 400, 400])
        crocodile_reader.show()
    app.exec()


run_app()

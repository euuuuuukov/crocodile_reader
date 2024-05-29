from PyQt6.QtWidgets import QApplication

from sys import argv

from app_database.database_methods import is_authenticated, write_log

from authentication.window import AuthWindow

from main_window.window import MainWindow


def run_app() -> None:
    try:
        app = QApplication(argv)
        if not is_authenticated():
            crocodile_reader = AuthWindow()
        else:
            crocodile_reader = MainWindow([0, 0, 400, 400])
        crocodile_reader.show()
        app.exec()
    except Exception as exc:
        write_log(f'{exc}, {type(exc)}')


run_app()

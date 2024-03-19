from PyQt6.QtGui import QIcon, QResizeEvent, QAction
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QPushButton, QLineEdit, QLabel, QPlainTextEdit, QPlainTextDocumentLayout

from ctypes import windll

from typing import Union

from app_database.database_methods import get_app_id

from txt_reader.txt_methods import open_file


class MainWindow(QMainWindow):
    def __init__(self, size: list[int]) -> None:
        super().__init__()

        windll.shell32.SetCurrentProcessExplicitAppUserModelID(get_app_id())

        self.setWindowTitle('Главная - CrocodileReader')
        self.setMinimumSize(400, 400)
        self.setGeometry(*size)
        self.setWindowIcon(QIcon('../assets/app_icon.png'))

        self.max_tab_number, self.active_tab = -1, -1
        self.tabs: list[list[Union[QPushButton, QPlainTextEdit]]] = []

        self.menubar = self.menuBar()

        self.main_actions = [QAction('&Открыть', self)]
        self.main_actions[0].triggered.connect(self.menu_open_clicked)
        self.main_actions[0].setCheckable(False)

        self.main_menubar = self.menubar.addMenu('&Меню')
        for action in self.main_actions:
            if type(action) is QAction:
                self.main_menubar.addAction(action)

    def menu_open_clicked(self) -> None:
        try:
            filename = QFileDialog.getOpenFileName(self, 'Открытие файла - CrocodileReader', 'C://',
                                                   'Все файлы (*.txt; *.doc; *.docx; *.xls; *.xlsx, *.csv);;'
                                                   'Текстовый документ (*.txt);; Документ Word-1997 (*.doc);;'
                                                   'Документ Word-2007 (*.docx);; Таблица Excel-1997 (*.xls);;'
                                                   'Таблица Excel-2007 (*.xlsx);; Таблица с разделителем (*.csv)')[0]
            with open(filename, 'r'):
                pass

            self.max_tab_number += 1
            if filename.endswith('.txt'):
                self.tabs.append([QPushButton(filename[filename.rfind('/') + 1:], self),
                                  QPlainTextEdit(open_file(filename), self)])

            self.tabs[-1][0].resize(80, 30)
            self.tabs[-1][0].move(80 * self.max_tab_number, self.menubar.height())
            self.tabs[-1][1].resize(self.width(), self.height() - self.menubar.height())
            self.tabs[-1][1].move(0, self.menubar.height() + 30)

            self.set_active_tab(self.max_tab_number)

        except FileNotFoundError:
            pass

    def set_active_tab(self, tab_number: int):
        self.active_tab = tab_number
        for tab in self.tabs:
            tab[0].hide()
            tab[1].hide()
        for sub in self.tabs[tab_number]:
            sub.show()
        self.setWindowTitle(self.tabs[tab_number][0].text())

    def resizeEvent(self, event: QResizeEvent) -> None:
        for tab in self.tabs:
            tab[1].resize(self.width(), self.height() - self.menubar.height() - 30)
            tab[1].move(0, self.menubar.height() + 30)

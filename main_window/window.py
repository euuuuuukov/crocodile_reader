from PyQt6.QtGui import QIcon, QPixmap, QResizeEvent, QAction
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QPushButton, QTextEdit, QLabel, QPlainTextEdit, QPlainTextDocumentLayout
from PyQt6.QtCore import Qt

from ctypes import windll

from typing import Union

from app_database.database_methods import get_app_id, get_last_dir, write_last_dir

from txt_reader.txt_methods import open_txt_file

from docx_reader.docx_methods import open_docx_file


class MainWindow(QMainWindow):
    def __init__(self, size: list[int]) -> None:
        super().__init__()

        windll.shell32.SetCurrentProcessExplicitAppUserModelID(get_app_id())

        self.setWindowTitle('Главная - CrocodileReader')
        self.setMinimumSize(400, 400)
        self.setGeometry(*size)
        self.setWindowIcon(QIcon('../assets/app_icon.png'))

        self.loading_label = QLabel('', self)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.hide()

        self.error_label = QLabel('', self)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet('font-size: 40px')
        self.error_label.hide()

        self.max_tab_number, self.active_tab = -1, -1
        self.tabs: list[list[Union[QPushButton, QPlainTextEdit, QTextEdit]]] = []

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
            self.loading_label.show()

            filepath = QFileDialog.getOpenFileName(self, 'Открытие файла - CrocodileReader', get_last_dir(),
                                                   'Все файлы (*.txt; *.doc; *.docx; *.xls; *.xlsx, *.csv);;'
                                                   'Текстовый документ (*.txt);; Документ Word-1997 (*.doc);;'
                                                   'Документ Word-2007 (*.docx);; Таблица Excel-1997 (*.xls);;'
                                                   'Таблица Excel-2007 (*.xlsx);; Таблица с разделителем (*.csv)')[0]
            with open(filepath, 'r'):
                pass

            write_last_dir(filepath[:filepath.rfind('/') + 1])
            filename = filepath[filepath.rfind('/') + 1:]
            if filepath.endswith('.txt'):
                self.tabs.append([QPushButton(filename, self), QPlainTextEdit(open_txt_file(filepath), self), filepath])
            elif filepath.endswith('.docx'):
                self.tabs.append([QPushButton(filename, self), QTextEdit('', self), filepath])
                self.tabs[-1][1].setHtml(open_docx_file(filepath))

            self.max_tab_number += 1

            self.tabs[-1][0].resize(80, 30)
            self.tabs[-1][0].move(80 * self.max_tab_number, self.menubar.height())
            self.tabs[-1][1].resize(self.width(), self.height() - self.menubar.height())
            self.tabs[-1][1].move(0, self.menubar.height())

            self.set_active_tab(self.max_tab_number)
            self.loading_label.hide()

        except FileNotFoundError:
            self.error_label.setText('Не удается найти указанный файл. Проверьте правильность имени файла.')
            self.error_label.show()
        except RuntimeError:
            self.error_label.setText('Недостаточно места на диске для открытия файла.')
            self.error_label.show()
        except Exception as exc:
            print(exc, type(exc))

    def set_active_tab(self, tab_number: int):
        self.active_tab = tab_number
        for tab in self.tabs:
            tab[1].hide()
        self.tabs[tab_number][1].show()
        self.setWindowTitle(self.tabs[tab_number][0].text() + ' - CrocodileReader')

    def resizeEvent(self, event: QResizeEvent) -> None:
        width, height = self.width(), self.height()
        menubar_height = self.menubar.height()

        self.loading_label.resize(self.width(), self.height() - menubar_height)
        self.loading_label.move(0, menubar_height)
        if width / (height - menubar_height) >= 1280 / 360:
            self.loading_label.setPixmap(QPixmap('../assets/loading.png').scaled(
                ((height - menubar_height) * 1280) // 360, height - menubar_height))
        else:
            self.loading_label.setPixmap(QPixmap('../assets/loading.png').scaled(width, (width * 360) // 1280))

        for tab in self.tabs:
            tab[1].resize(self.width(), self.height() - menubar_height)
            tab[1].move(0, menubar_height)

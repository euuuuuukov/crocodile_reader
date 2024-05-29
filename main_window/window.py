from PyQt6.QtGui import QIcon, QPixmap, QResizeEvent, QAction
from PyQt6.QtWidgets import QMainWindow, QToolBar, QPushButton, QTextEdit, QLabel, QPlainTextEdit
from PyQt6.QtWidgets import QFileDialog, QInputDialog
from PyQt6.QtCore import Qt, QSize

from ctypes import windll

from typing import Union

from keyboard import press_and_release

from app_database.database_methods import (get_app_id, get_last_dir, write_last_dir, write_log,
                                           error_style, app_style)

from docx_reader.docx_methods import open_docx_file, save_docx_file

from bug_report.window import BugReportWindow

from main_window.settings_window import SettingsWindow


def cancel_hotkey() -> None:
    press_and_release('Ctrl+Z')


def return_hotkey() -> None:
    press_and_release('Ctrl+Y')


class MainWindow(QMainWindow):
    def __init__(self, size: list[int]) -> None:
        try:
            super().__init__()

            windll.shell32.SetCurrentProcessExplicitAppUserModelID(get_app_id())

            self.setWindowTitle('Главная - CrocodileReader')
            self.setMinimumSize(400, 400)
            self.setGeometry(*size)
            self.setWindowIcon(QIcon('../assets/app_icon.png'))
            self.setStyleSheet(app_style())

            self.loading_label = QLabel('', self)
            self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.loading_label.hide()

            self.error_label = QLabel('', self)
            self.error_label.setStyleSheet(error_style())
            self.error_label.hide()

            self.max_tab_number, self.active_tab = -1, -1
            self.tabs: list[list[Union[QPushButton, QPlainTextEdit, QTextEdit, str]]] = []

            self.menubar = self.menuBar()

            self.main_actions = [QAction('Открыть', self), QAction('Сохранить', self), QAction('Сохранить как', self),
                                 QAction('Настройки', self), QAction('Отправить отчет об ошибке', self)]
            self.main_actions_shortcuts = ['Ctrl+O', 'Ctrl+S', 'Ctrl+Shift+S', 'Ctrl+Alt+S', 'Ctrl+Alt+B']

            for action_number in range(len(self.main_actions)):
                self.main_actions[action_number].setShortcut(self.main_actions_shortcuts[action_number])
                self.main_actions[action_number].setCheckable(False)

            self.main_actions[0].triggered.connect(self.open_file)
            self.main_actions[1].triggered.connect(self.save_file)
            self.main_actions[2].triggered.connect(self.save_as_file)
            self.main_actions[3].triggered.connect(self.settings)
            self.main_actions[4].triggered.connect(self.bug_report)

            self.main_menubar = self.menubar.addMenu('Меню')
            self.main_menubar.addActions(self.main_actions[:3])
            self.main_menubar.addSeparator()
            self.main_menubar.addAction(self.main_actions[3])
            self.main_menubar.addSeparator()
            self.main_menubar.addAction(self.main_actions[4])

            self.toolbar = QToolBar('Toolbar', self)
            self.toolbar.setIconSize(QSize(16, 16))
            self.toolbar.setMovable(False)
            self.toolbar.hide()

            self.toolbar_buttons = [QAction(QIcon('../assets/edit-bold.png'), 'Полужирный', self),
                                    QAction(QIcon('../assets/edit-italic.png'), 'Курсив', self),
                                    QAction(QIcon('../assets/edit-underline.png'), 'Подчеркнутый', self),
                                    QAction(QIcon('../assets/arrow-curve-180-left.png'), 'Отменить', self),
                                    QAction(QIcon('../assets/arrow-curve.png'), 'Вернуть', self),
                                    QAction(QIcon('../assets/table--plus.png'), 'Добавить таблицу', self)]
            self.toolbar_buttons_shortcuts = ['Ctrl+B', 'Ctrl+I', 'Ctrl+U', 'Ctrl+Z', 'Ctrl+Y', 'Ctrl+T']

            for button_number in range(len(self.toolbar_buttons)):
                self.toolbar_buttons[button_number].setShortcut(self.toolbar_buttons_shortcuts[button_number])
                self.toolbar_buttons[button_number].setText(self.toolbar_buttons[button_number].text() + ' (' +
                                                            self.toolbar_buttons_shortcuts[button_number] + ')')
            self.toolbar.addActions(self.toolbar_buttons)

            for biu in self.toolbar_buttons[:3]:
                biu.triggered.connect(self.set_biu)
            self.toolbar_buttons[3].triggered.connect(cancel_hotkey)
            self.toolbar_buttons[4].triggered.connect(return_hotkey)
            self.toolbar_buttons[5].triggered.connect(self.insert_table)

            self.addToolBar(self.toolbar)

            self.menubar_height = self.menubar.height()
            self.toolbar_height = self.toolbar.height()

            self.bug_report_window = BugReportWindow()
            self.bug_report_window.close()

            self.settings_window = SettingsWindow()
            self.settings_window.close()
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def open_file(self) -> None:
        try:
            filepath = QFileDialog.getOpenFileName(self, 'Открыть - CrocodileReader', get_last_dir(),
                                                   'Все файлы (*.txt; *.doc; *.docx);; Текстовый документ (*.txt);; '
                                                   'Документ Word-1997 (*.doc);; Документ Word-2007 (*.docx)')[0]
            if filepath == '':
                return
            with open(filepath, 'r'):
                pass

            for tab_number in range(len(self.tabs)):
                if filepath == self.tabs[tab_number][-1]:
                    self.set_active_tab(tab_number)
                    return

            self.loading_label.show()

            write_last_dir(filepath[:filepath.rfind('/') + 1])
            filename = filepath[filepath.rfind('/') + 1:]
            if filepath.endswith('.docx'):
                self.tabs.append([QPushButton(filename, self), QTextEdit('', self), filepath])
                self.tabs[-1][1].setHtml(open_docx_file(filepath))

            self.max_tab_number += 1

            self.tabs[-1][0].resize(100, 30)
            self.tabs[-1][0].move(100 * self.max_tab_number, self.menubar_height + self.toolbar_height)
            self.tabs[-1][0].clicked.connect(self.button_set_active_tab)
            self.tabs[-1][0].show()

            self.tabs[-1][1].resize(self.width(), self.height() - self.menubar_height - self.toolbar_height - 30)
            self.tabs[-1][1].move(0, self.menubar_height + self.toolbar_height + 30)
            self.tabs[-1][1].setStyleSheet('font: 14pt "Times New Roman";')

            self.set_active_tab(self.max_tab_number)
            self.loading_label.hide()
        except FileNotFoundError:
            self.error_label.setText('Не удается найти указанный файл.\nПроверьте правильность имени файла.')
            self.error_label.show()
        except RuntimeError:
            self.error_label.setText('Недостаточно места на диске для открытия файла.')
            self.error_label.show()
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def set_active_tab(self, tab_number: int):
        try:
            self.active_tab = tab_number
            for tab in self.tabs:
                tab[1].hide()
            self.tabs[tab_number][1].show()
            self.setWindowTitle(self.tabs[tab_number][0].text() + ' - CrocodileReader')
            self.toolbar.show()
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def save_file(self) -> None:
        try:
            save_docx_file(self.tabs[self.active_tab][2], self.tabs[self.active_tab][1].toHtml())
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def save_as_file(self) -> None:
        try:
            save_docx_file(QFileDialog.getSaveFileName(
                self, 'Сохранить как - CrocodileReader', get_last_dir(),
                'Все файлы (*.txt; *.doc; *.docx);; Текстовый документ (*.txt);; '
                'Документ Word-1997 (*.doc);; Документ Word-2007 (*.docx)')[0],
                           self.tabs[self.active_tab][1].toHtml())
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def settings(self) -> None:
        try:
            self.settings_window.show()
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def bug_report(self) -> None:
        try:
            self.bug_report_window = BugReportWindow()
            self.bug_report_window.show()
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def button_set_active_tab(self) -> None:
        try:
            self.set_active_tab([tab[0] for tab in self.tabs].index(self.sender()))
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def set_biu(self) -> None:
        try:
            tag = self.sender().text()[-2]
            self.tabs[self.active_tab][1].insertHtml(
                f'<{tag}>' + self.tabs[self.active_tab][1].textCursor().selectedText() + f'</{tag}>')
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

    def insert_table(self) -> None:
        try:
            rows, ok = QInputDialog.getInt(
                self, 'Создание таблицы - CrocodileReader', 'Введите количество строк:', value=3, min=1)
            if ok:
                cols, ok = QInputDialog.getInt(
                    self, 'Создание таблицы - CrocodileReader', 'Введите количество столбцов:', value=3, min=1)
                if ok:
                    self.tabs[self.active_tab][1].textCursor().insertTable(int(rows), int(cols))
        except Exception as exc:
            print(exc, type(exc))

    def resizeEvent(self, event: QResizeEvent) -> None:
        try:
            width, height = self.width(), self.height()
            self.menubar_height = self.menubar.height()
            self.toolbar_height = self.toolbar.height()

            self.error_label.resize(width, height - self.menubar_height - self.toolbar_height - 30)
            self.error_label.move(0, self.menubar_height + self.toolbar_height + 30)

            self.loading_label.resize(width, height - self.menubar_height - self.toolbar_height - 30)
            self.loading_label.move(0, self.menubar_height + self.toolbar_height + 30)
            if width / (height - self.menubar_height) >= 1280 / 360:
                self.loading_label.setPixmap(QPixmap('../assets/loading.png').scaled(
                    ((height - self.menubar_height) * 1280) // 360, height - self.menubar_height))
            else:
                self.loading_label.setPixmap(QPixmap('../assets/loading.png').scaled(width, (width * 360) // 1280))

            for tab in self.tabs:
                tab[1].resize(width, height - self.menubar_height - self.toolbar_height - 30)
                tab[1].move(0, self.menubar_height + self.toolbar_height + 30)
        except Exception as exc:
            write_log(f'{exc}, {type(exc)}')

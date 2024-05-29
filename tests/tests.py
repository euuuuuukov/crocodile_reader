from unittest import TestCase, main

from json import dump, load

from random import choice, randint

from app_database.database_methods import *


class CrocodileReaderTestCase(TestCase):
    def test_get_app_id(self) -> None:
        self.assertEqual(get_app_id(), 'crocodile_reader.euuuuuukov')

    def test_is_authenticated(self) -> None:
        self.assertEqual(is_authenticated(), True)

    def test_get_user_data_from_app_database(self) -> None:
        self.assertEqual([get_user_data_from_app_database(data_type) for data_type in ['id', 'name', 'surname']],
                         ['1', 'Евгений', 'Коваленко'])

    def test_get_last_dir(self) -> None:
        string = ''.join([choice('1234567890qwertyuioplkjhgfdsazxcvbnm][;.,/') for _ in range(randint(50, 100))])
        write_last_dir(string)
        self.assertEqual(get_last_dir(), string)

    def test_write_last_dir(self) -> None:
        string = ''.join([choice('1234567890qwertyuioplkjhgfdsazxcvbnm][;.,/') for _ in range(randint(50, 100))])
        write_last_dir(string)
        with open('../app_database/app_info.json', 'r', encoding='utf-8') as app_info:
            self.assertEqual(string, load(app_info)['other_info']['last_dir'])

    def test_write_log(self) -> None:
        string = ''.join([choice('1234567890qwertyuioplkjhgfdsazxcvbnm][;.,/') for _ in range(randint(50, 100))])
        write_log(string)
        with open('../app_database/log.log', 'r', encoding='utf-8') as log_file:
            self.assertEqual(log_file.readline().split()[2], string)

    def test_active_button_style(self) -> None:
        with open('../interface/active_button_style.txt', 'w', encoding='utf-8') as style:
            style.write('border: 2px solid rgb(18, 185, 0)')
        self.assertEqual(active_button_style(), 'border: 2px solid rgb(18, 185, 0)')

    def test_app_style(self) -> None:
        self.assertEqual(app_style().split(), '''QWidget {
    background-color: rgb(31, 48, 31);
}
QPushButton {
    background-color: rgb(118, 232, 118);
}
QLineEdit {
    background-color: rgb(255, 255, 255);
}
QTextEdit {
    background-color: rgb(255, 255, 255);
}
QPlainTextEdit {
    background-color: rgb(255, 255, 255);
}
QMenuBar {
    background-color: rgb(255, 255, 255);
}
QToolBar {
    background-color: rgb(255, 255, 255);
}
QLabel {
    qproperty-alignment: AlignCenter;
}'''.split())

    def test_change_color(self) -> None:
        change_color(['QPlainTextEdit', 'QToolBar'], [255, 255, 255])
        lines = app_style().split('\n')
        self.assertEqual([lines[13].split(), lines[19].split()],
                         [['background-color:', 'rgb(255,', '255,', '255);'] for i in range(2)])


if __name__ == '__main__':
    main()

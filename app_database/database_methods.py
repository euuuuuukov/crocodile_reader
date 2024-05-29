from json import dump, load

from datetime import datetime

from cloud_database.spreadsheets_methods import get_user_data


def get_app_id() -> str:
    with open('../app_database/app_info.json', 'r', encoding='utf-8') as app_info:
        return load(app_info)['app_info']['app_id']


def is_authenticated() -> bool:
    with open('../app_database/app_info.json', 'r', encoding='utf-8') as app_info:
        return load(app_info)['user_info']['is_authenticated']


def rewrite_authentication(index: str) -> None:
    with open('../app_database/app_info.json', 'r', encoding='utf-8') as app_info:
        d = load(app_info)
        d['user_info']['is_authenticated'] = True
        data, subs = get_user_data(index), ['id', 'name', 'surname', 'email', 'password']
        for i in range(5):
            d['user_info'][subs[i]] = data[i]
    with open('../app_database/app_info.json', 'w', encoding='utf-8') as app_info:
        dump(d, app_info, indent=4)


def get_user_data_from_app_database(data_type: str) -> str:
    with open('../app_database/app_info.json', 'r', encoding='utf-8') as app_info:
        return load(app_info)['user_info'][data_type]


def get_last_dir() -> str:
    with open('../app_database/app_info.json', 'r', encoding='utf-8') as app_info:
        return load(app_info)['other_info']['last_dir']


def write_last_dir(last_dir: str) -> None:
    with open('../app_database/app_info.json', 'r', encoding='utf-8') as app_info:
        info = load(app_info)
        info['other_info']['last_dir'] = last_dir
    with open('../app_database/app_info.json', 'w', encoding='utf-8') as app_info:
        dump(info, app_info, indent=4)


def write_log(text: str) -> None:
    with open('../app_database/log.log', 'a', encoding='utf-8') as log_file:
        log_file.write(f'{datetime.now()}: {text}\n')


def error_style() -> str:
    return 'color: rgb(255, 0, 0);\nfont-size: 12px;'


def active_button_style() -> str:
    with open('../interface/active_button_style.txt', 'r', encoding='utf-8') as active_button_style_file:
        return active_button_style_file.read()


def inactive_button_style() -> str:
    return 'border: 0px'


def app_style() -> str:
    with open('../interface/app_style.txt', 'r', encoding='utf-8') as app_style_file:
        return app_style_file.read()


def change_color(objects: list[str], colors: list[int]) -> None:
    with open('../interface/app_style.txt', 'r', encoding='utf-8') as app_style_file:
        style = app_style_file.read()
    for i in range(len(objects)):
        start_pos = style.find(objects[i])
        end_pos = style.find('}', start_pos)
        style = (style[:start_pos] + objects[i] + ' {\n\t' +
                 f'background-color: rgb({colors[0]}, {colors[1]}, {colors[2]});\n' + style[end_pos:])
    with open('../interface/app_style.txt', 'w', encoding='utf-8') as app_style_file:
        app_style_file.write(style)

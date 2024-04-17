from json import dump, load

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


def get_email() -> str:
    with open('../app_database/app_info.json', 'r', encoding='utf-8') as app_info:
        return load(app_info)['user_info']['email']


def get_last_dir() -> str:
    with open('../app_database/app_info.json', 'r', encoding='utf-8') as app_info:
        return load(app_info)['other_info']['last_dir']


def write_last_dir(last_dir: str) -> None:
    with open('../app_database/app_info.json', 'r', encoding='utf-8') as app_info:
        info = load(app_info)
        info['other_info']['last_dir'] = last_dir
    with open('../app_database/app_info.json', 'w', encoding='utf-8') as app_info:
        dump(info, app_info, indent=4)

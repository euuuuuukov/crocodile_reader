from json import load, dump


def is_authenticated() -> bool:
    with open('../database/app_info.json', 'r', encoding='utf-8') as app_info:
        return load(app_info)['user_info']['is_authenticated']


def rewrite_authentication() -> None:
    with open('../database/app_info.json', 'w', encoding='utf-8') as app_info:
        d = load(app_info)
        d['user_info']['is_authenticated'] = True
        dump(d, app_info, indent=4)

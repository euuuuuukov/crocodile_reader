from cloud_database.spreadsheets_methods import check_email


def compliance_get_code(name: str, surname: str, email: str) -> list[str]:
    returned = ['', '']
    name_const = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM- ' \
                 'йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ'
    email_const = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM.-_@1234567890'
    f = True
    if name == '' or surname == '':
        f = False
    else:
        for symbol in name + surname:
            if symbol not in name_const:
                f = False
                break
    if not f:
        returned[0] = 'Имя и фамилия могут состоять только из букв и дефиса'
    if email == 'email':
        returned[1] = 'Некорректный e-mail'
    elif not check_email(email):
        returned[1] = 'Этот e-mail уже используется'
    else:
        f = True
        if email.count('@') == 1:
            if '.' in email[email.find('@') + 1:]:
                for symbol in email:
                    if symbol not in email_const:
                        print(symbol)
                        f = False
                        break
            else:
                f = False
        else:
            f = False
        if not f:
            returned[1] = 'Некорректный e-mail'
    return returned


def compliance_sign_up(name: str, surname: str, email: str,
                       code: str, password: str, repeat_password: str) -> list[str]:
    returned = ['', '']
    try:
        with open('../app_database/authentication_code.txt', 'r', encoding='utf-8') as authentication_code:
            if code != authentication_code.read():
                returned[0] = 'Неправильный код'
    except FileNotFoundError:
        returned[0] = 'Сначала получите подтверждающий код'
    if len(password) < 8 or len(repeat_password) < 8:
        returned[1] = 'Пароль должен содержать хотя бы 8 символов'
    elif password != repeat_password:
        returned[1] = 'Пароли должны совпадать'
    return compliance_get_code(name, surname, email) + returned

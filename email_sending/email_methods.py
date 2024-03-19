from smtplib import SMTPRecipientsRefused, SMTPSenderRefused, SMTPServerDisconnected

from random import choice

from email_sending.setup_email import EmailSender


smtp_object = EmailSender()


def send_authentication_email(address: str, name: str, surname: str) -> str:
    code = ''.join([choice([str(i) for i in range(10)]) for _ in range(6)])
    try:
        smtp_object.send_email(address, f'Здравствуйте, {name} {surname}! Ваш код подтверждения: <b>{code}</b>. '
                                        f'Введите его в соответствующее поле в приложении.', 'Подтверждение аккаунта')
        returned = 'Код подтверждения отправлен на e-mail'
        with open('../app_database/authentication_code.txt', 'w', encoding='utf-8') as authentication_code:
            authentication_code.write(code)
    except SMTPRecipientsRefused:
        returned = 'Некорректный e-mail'
    except SMTPSenderRefused:
        returned = 'Почтовый сервер отключен. Отправьте отчет об ошибке'
    except SMTPServerDisconnected:
        returned = 'Проверьте подключение к сети Интернет'
    except Exception as exception:
        with open('../app_database/log.log', 'a', encoding='utf-8') as log:
            log.write(f'{exception}\n{type(exception)}\n\n')
        returned = 'Ошибка отправки. Отправьте отчет об ошибке'
    return returned

from smtplib import SMTPRecipientsRefused, SMTPSenderRefused, SMTPServerDisconnected

from random import choice

from email_sending.setup_email import EmailSender

from app_database.database_methods import write_log


try:
    smtp_object = EmailSender()
except Exception as exception:
    write_log(f'{exception}, {type(exception)}')


def send_authentication_email(address: str, name: str, surname: str) -> str:
    try:
        code = ''.join([choice([str(i) for i in range(10)]) for _ in range(6)])
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
    except Exception as exc:
        write_log(f'{exc}, {type(exc)}')
        returned = 'Ошибка отправки. Отправьте отчет об ошибке'
    return returned

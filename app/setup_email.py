from smtplib import SMTP, SMTPRecipientsRefused

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from random import choice

from config.keys import email_info


class EmailSender:
    def __init__(self) -> None:
        self.smtp = SMTP('smtp-mail.outlook.com', 587)
        self.smtp.starttls()
        self.smtp.login(email_info['email'], email_info['password'])

    def send_email(self, address: str, text: str, subject: str) -> None:
        message = MIMEMultipart()
        message['From'], message['To'], message['Subject'] = email_info['email'], address, subject
        message.attach(MIMEText(text, 'html'))
        self.smtp.sendmail(email_info['email'], address, message.as_string())

    def terminate(self) -> None:
        self.smtp.quit()


def send_authentication_email(address: str, name: str, surname: str) -> tuple[str, str]:
    code = ''.join([choice([str(i) for i in range(10)]) for _ in range(6)])
    print(code)
    try:
        smtp_object = EmailSender()
        smtp_object.send_email(address, f'Здравствуйте, {name} {surname}! Ваш код подтверждения: <b>{code}</b>. '
                                        f'Введите его в соответствующее поле в приложении.', 'Подтверждение аккаунта')
        returned = 'Код подтверждения отправлен на e-mail'
        smtp_object.terminate()
    except SMTPRecipientsRefused:
        returned = 'Некорректный e-mail (501 Error)'
    except Exception as exception:
        with open('../config/log.log', 'a', encoding='utf-8') as log:
            log.write(f'{exception}\n{type(exception)}\n\n')
        returned = 'Ошибка отправки. Повторите попытку позже'
    return code, returned

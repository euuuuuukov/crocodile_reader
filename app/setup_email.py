from smtplib import SMTP, SMTPRecipientsRefused

from config.email import email_info

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:
    def __init__(self) -> None:
        self.smtp = SMTP('smtp-mail.outlook.com', 587)
        self.smtp.starttls()
        self.smtp.login(email_info['email'], email_info['password'])

    def send_email(self, address: str, text: str) -> None:
        message = MIMEMultipart()
        message['From'], message['To'], message['Subject'] = email_info['email'], address, 'Подтверждение аккаунта'
        message.attach(MIMEText(text, 'html'))
        self.smtp.sendmail(email_info['email'], address, message.as_string())

    def terminate(self) -> None:
        self.smtp.quit()


def send_authentication_email(address: str, name: str, surname: str, code: int) -> str:
    smtp_object = EmailSender()
    try:
        smtp_object.send_email(address, f'Здравствуйте, {name} {surname}!\nВаш код подтверждения: <b>{code}</b>. '
                                        f'Введите его в соответствующее поле в приложении.')
        returned = 'Код подтверждения отправлен на адрес электронной почты'
    except SMTPRecipientsRefused:
        returned = 'Некорректный адрес электронной почты'
    smtp_object.terminate()
    return returned

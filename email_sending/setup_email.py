from smtplib import SMTP

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.app_keys import email_info


class EmailSender:
    def __init__(self) -> None:
        self.smtp = SMTP('smtp-mail.outlook.com', 587)
        self.smtp.starttls()
        with open('../config/app_keys.py', 'r', encoding='utf-8') as app_keys:
            self.from_email, self.from_password = email_info['email_dir'], email_info['password']
        self.smtp.login(self.from_email, self.from_password)

    def send_email(self, address: str, text: str, subject: str) -> None:
        message = MIMEMultipart()
        message['From'], message['To'], message['Subject'] = self.from_email, address, subject
        message.attach(MIMEText(text, 'html'))
        self.smtp.sendmail(self.from_email, address, message.as_string())

    def terminate(self) -> None:
        self.smtp.quit()

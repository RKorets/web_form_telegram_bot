import smtplib
from email.mime.text import MIMEText


def send_email(message, to_email):
    sender = 'YOU_MAIL'
    password = 'YOU_MAIL_PASSWORD'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Sybject"] = 'APP-Telegram-Sender: Answer for you appel'
        server.sendmail(sender, to_email, msg.as_string())

        return True
    except Exception as ex:
        return False
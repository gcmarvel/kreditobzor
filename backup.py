import datetime
import smtplib
import ssl
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

absolute_path = os.path.dirname(os.path.abspath(__file__))
db_path = absolute_path + '/frodo666/kreditobzor/db.sqlite3'

today = datetime.date.today()
weekday = today.weekday()

if weekday == 0:

    password = "tggkuvdwokxrpvaq"
    sender = "kreditobzor_internal@mail.ru"
    receiver = "kreditobzor@mail.ru"
    body = ""

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = "Свежие базы данных завезли"
    message.attach(MIMEText(body, "plain"))


    context = ssl.create_default_context()

    with open(db_path, 'rb') as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        "attachment; filename=db.sqlite3",
    )

    message.attach(part)

    text = message.as_string()

    with smtplib.SMTP_SSL("smtp.mail.ru", 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, text)

#!/usr/bin/env python

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.Header import Header

<<<<<<< HEAD
# send NBA daily report from email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("programmingemail0930@gmail.com", "pXf-dqL-DBX-v2Z")

# FROM = 'monty@python.com'
# TO = ['jon@mycompany.com']  # must be a list
msg = MIMEMultipart('alternative')
SUBJECT = "NBA daily report!\n"
msg['Subject'] = Header(SUBJECT)
=======

with open('config.json') as config:
    config_data = json.load(config)
    smtp_host = config_data['smtp_host']
    smtp_port = config_data['smtp_port']
    email = config_data['email']
    password = config_data['password']

server = smtplib.SMTP(smtp_host, smtp_port)
server.starttls()
server.login(email, password)
>>>>>>> d9907004d8ae44214c42827210bcc2b3f9cb6eb9


<<<<<<< HEAD
# msg = """
# From: {0}
# To: {1}
# Subject: {2}
#
# """.format(FROM, ", ".join(TO), SUBJECT)
msg.attach(MIMEText(open('nba_report.txt', 'rb').read()))
server.sendmail("programmingemail0930@gmail.com", "tsoliangwu0130@gmail.com", msg.as_string())
=======
SUBJECT = "NBA daily report!"
TEXT = "This message was sent with Python's smtplib."

msg = """
From: {}
To: {}
Subject: {}
{}
""".format(FROM, ", ".join(TO), SUBJECT, TEXT)

server.sendmail(email, "luckymanyo@gmail.com", msg)
>>>>>>> d9907004d8ae44214c42827210bcc2b3f9cb6eb9
server.quit()

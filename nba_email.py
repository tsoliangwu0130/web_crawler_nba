#!/usr/bin/env python

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.Header import Header

# send NBA daily report from email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("programmingemail0930@gmail.com", "pXf-dqL-DBX-v2Z")

# FROM = 'monty@python.com'
# TO = ['jon@mycompany.com']  # must be a list
msg = MIMEMultipart('alternative')
SUBJECT = "NBA daily report!\n"
msg['Subject'] = Header(SUBJECT)


# msg = """
# From: {0}
# To: {1}
# Subject: {2}
#
# """.format(FROM, ", ".join(TO), SUBJECT)
msg.attach(MIMEText(open('nba_report.txt', 'rb').read()))
server.sendmail("programmingemail0930@gmail.com", "tsoliangwu0130@gmail.com", msg.as_string())
server.quit()

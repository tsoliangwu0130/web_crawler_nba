#!/usr/bin/env python

import json
import smtplib


with open('config.json') as config:
    config_data = json.load(config)
    smtp_host = config_data['smtp_host']
    smtp_port = config_data['smtp_port']
    email = config_data['email']
    password = config_data['password']

server = smtplib.SMTP(smtp_host, smtp_port)
server.starttls()
server.login(email, password)

FROM = 'monty@python.com'
TO = ['jon@mycompany.com']  # must be a list

SUBJECT = "NBA daily report!"
TEXT = "This message was sent with Python's smtplib."

msg = """
From: {}
To: {}
Subject: {}
{}
""".format(FROM, ", ".join(TO), SUBJECT, TEXT)

server.sendmail(email, "luckymanyo@gmail.com", msg)
server.quit()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.Header import Header


def send_email(subject, filename):
    with open('config.json') as config:
        config_data = json.load(config)
        smtp_host = config_data['smtp_host']
        smtp_port = config_data['smtp_port']
        email = config_data['email']
        password = config_data['password']

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(email, password)

        msg = MIMEMultipart()
        msg['Subject'] = Header(subject)

        msg.attach(MIMEText(open(filename, 'rb').read()))
        server.sendmail("programmingemail0930@gmail.com", "luckymanyo@gmail.com", msg.as_string())

        server.quit()

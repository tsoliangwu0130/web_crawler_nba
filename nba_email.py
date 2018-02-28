#!/usr/bin/env python

import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("luckymanyaya@gmail.com", "a45235187")


FROM = 'monty@python.com'
TO = ['jon@mycompany.com']  # must be a list

SUBJECT = "NBA daily report!"
TEXT = "This message was sent with Python's smtplib."

msg = """
From: %s
To: %s
Subject: %s
%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

server.sendmail("luckymanyaya@gmail.com", "luckymanyo@gmail.com", msg)
server.quit()

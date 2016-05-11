#!/usr/bin/env python

"""
Krish Munot
May 9, 2016
The things I do instead of studying for finals :D
"""

import urllib, json
import os, smtplib
import random

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Example SMTP server - gmail.com
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
DIRECTORY = "/Directory/to/save/image/temporarily"

SENDER_EMAIL_ADDRESS = 'xxxxxx@mail.com'
SENDER_EMAIL_SECRET = "xxxxxx"
RECIPIENT_ADDRESSES = ["address1@mail.org"]

EMAIL_SENDING_HOUR = 8 # 8:00am
EMAIL_SUBJECT = "Rise and Shine!"

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR

class EmailSender(object):

    def __init__(self, subject):
        # Authentication information
        self._sender = SENDER_EMAIL_ADDRESS
        self._password = SENDER_EMAIL_SECRET

        # Message contents
        self._subject = subject
        self._init_message()

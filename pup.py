#!/usr/bin/env python

"""
Krish Munot
May 8, 2016
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

"""
=================
class EmailSender
=================
"""

class EmailSender(object):
    """    An SMTP email sending client that can send an email with
        attachments to multiple people.
    """

    def __init__(self, subject):
        # Authentication information
        self._sender = SENDER_EMAIL_ADDRESS
        self._password = SENDER_EMAIL_SECRET

        # Message contents
        self._subject = subject
        self._init_message()
        
    def _init_message(self):
        """
        MODIFIES: self.msg
        EFFECTS:  Creates an email message with the given subject and message.
        """
        self.msg = MIMEMultipart()
        self.msg['Subject'] = self._subject
        self.msg['From'] = self._sender
        
    def _attach_message_text(self, html_message):
        """
        MODIFIES: self.msg
        EFFECTS:  Attaches the given text to the email message.
        """
        part = MIMEText('html', "html")
        part.set_payload(html_message)
        self.msg.attach(part)
        
    # ======
    # PUBLIC
    # ======

    def attach_image(self, image_filename):
        """
        REQUIRES: image_filename is a file that exists in the current directory
        MODIFIES: self.msg
        EFFECTS:  Attaches the image with the given filename to self.msg.
        """
        path = os.path.join(DIRECTORY, image_filename)

        img = MIMEImage(open(path, 'rb').read(), _subtype="gif")
        img.add_header('Content-Disposition', 'attachment', filename=image_filename)
        self.msg.attach(img)

    def create_session_and_send(self):
        """
        REQUIRES: Valid connection to the Gmail SMTP server
        EFFECTS:  Sends the message to the given recipient.
        """
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        session.ehlo()
        session.starttls()
        session.login(self._sender, self._password)
        for recipient in RECIPIENT_ADDRESSES:
            self.msg['To'] = recipient
            session.sendmail(self._sender, recipient, self.msg.as_string())
        session.quit()
        
class MorningPuppiesSender(EmailSender):
    """ MorningPuppies supplies all the methods to send an email of a cute
        animal each morning to everyone on an email list.
    """

    # =======
    # PRIVATE
    # =======

    def __init__(self, subject):
        EmailSender.__init__(self, subject)
        self.cute_picture_filename = ''
        self.extension = ''
        self.caption = ''

    def _retrieve_daily_picture(self):
        """
        REQUIRES: Connection to the internet is good.
        MODIFIES: The file cutePicture
        EFFECTS:  Saves the top imgur post from r/aww into the current
                  directory,
        """
        # URL of the top r/aww posts from Reddit
        aww_url = "http://www.reddit.com/r/aww/top.json"
        response = urllib.urlopen(aww_url)
        data = json.loads(response.read())

        # Retrieve picture link and reate filename
        imgur_link = data["data"]["children"][0]["data"]["url"]
        self.caption = "<h3>\"" + data["data"]["children"][0]["data"]["title"] + "\"</h3>"
        self.extension = imgur_link[imgur_link.rfind('.'):]
        self.cute_picture_filename = "cutePicture" + self.extension

        # Save the picture
        urllib.urlretrieve(imgur_link, filename=self.cute_picture_filename)
    

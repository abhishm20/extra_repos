#!/usr/bin/env python
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import httplib2
import shutil
import oauth2client
import pandas as pd
from apiclient import errors, discovery
from oauth2client import client, tools

APPLICATION_NAME = 'pymailer'

# Internal constant
SCOPES = 'https://www.googleapis.com/auth/gmail.send'

# Home directory
HOME_DIR = os.path.expanduser('~')

# Current directory
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# Configuration path (HOME/.pymailer)
CONF_PATH = os.path.join(HOME_DIR, '.' + APPLICATION_NAME)

CREDENTIAL_FILE_NAME = 'credentials.json'
SECRET_FILE_NAME = "client_secret.json"

SECRET_FILE_PATH = os.path.join(CURRENT_DIR, SECRET_FILE_NAME)
CREDENTIAL_FILE_PATH = os.path.join(CONF_PATH, CREDENTIAL_FILE_NAME)

SENDER_EMAIL_ID = 'Ravi Verkya <ravi@daybox.in>'

# Github link
GITHUB_LINK = "https://github.com/abhishm20/pymailer"


# colors
class colors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Global variable
parser = {}


def _get_credentials():
    store = oauth2client.file.Storage(CREDENTIAL_FILE_PATH)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(SECRET_FILE_PATH, SCOPES)
        flow.user_agent = APPLICATION_NAME
        parser.add_argument("--noauth_local_webserver", action='store_true', default=True)
        parser.add_argument("--logging_level", default='ERROR')
        parser.add_argument("--auth_host_name", default='localhost')
        parser.add_argument("--auth_host_port", default=[8080, 8090])
        flags = parser.parse_args(['--noauth_local_webserver'])
        credentials = tools.run_flow(flow, store, flags=flags)
        print '%sStoring credentials to %s%s' % (colors.BOLD, CREDENTIAL_FILE_PATH, colors.END)
    return credentials


def _send_message(sender, to, subject, msgHtml, msgPlain):
    credentials = _get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message1 = _create_message(sender, to, subject, msgHtml, msgPlain)
    return _send_message_internal(service, "me", message1)


def _send_message_internal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print '%sSuccessfully sent%s' % (colors.SUCCESS, colors.END)
        print '%smail message id: %s%s' % (colors.BOLD, message['id'], colors.END)
        return message['id']
    except errors.HttpError, error:
        print '%serror: %s%s' % (colors.ERROR, error, colors.END)


def _create_message(sender, to, subject, msg_html, msg_plain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msg_plain, 'plain'))
    msg.attach(MIMEText(msg_html, 'html'))
    return {'raw': base64.urlsafe_b64encode(msg.as_string())}


def _send_email(email, subject, body):
    to = email
    sender = SENDER_EMAIL_ID
    subject = subject
    msg_html = body
    return _send_message(sender, to, subject, msg_html, '')


def send(email, subject, body):
    _send_email(email, subject, body)


# Validation error class
class ValidationError(Exception):
    def __init__(self, message, errors=[]):
        # Call the base class constructor with the parameters it needs
        super(ValidationError, self).__init__(message)
        # Now for your custom code...
        self.errors = errors


# Command line arguments interpreter
def getopts(argv):
    try:
        opts = {}
        while argv:
            if argv[0][0] == '-':
                opts[argv[0]] = argv[1]
            argv = argv[1:]
        return opts
    except IndexError:
        print '%sInvalid argument(s)%s' % (colors.ERROR, colors.END)
        exit(-1)


def send_email(name, email):
    print "%smail-data: %s %s%s" % (colors.BLUE, name, email, colors.END)
    subject = "POSO App For %s : Control Food Cost and Streamline Purchase" % name
    body = """
    Hi {},
    <br><br>
    Did you get a chance to go through the previous mail?  
    <br><br>
    I firmly believe that POSO can help you streamline your raw material purchases. 
    <br><br>
    I would be grateful if you could indicate a convenient time to meet in the coming week. 
    <br><br>
    Regards,<br>
    Ravi Verkya<br>
    Team POSO<br>
    +91-9891756638<br>
    """.format(str(name))
    send(email, subject, body)


if __name__ == '__main__':
    xl = pd.ExcelFile("restaurant.xlsx")
    df = xl.parse('sheet')
    for index, row in df.iterrows():
        name = row['Restaurant Name']
        email = row['Email']
        send_email(name, email)
        time.sleep(1)

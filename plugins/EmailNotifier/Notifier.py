import re
import ssl
from smtplib import SMTP
from email.mime.text import MIMEText
from time import time
from BaseNotifier import BaseNotifier
import config

class EmailNotifier(BaseNotifier):
    regex = re.compile('^(?:mailto:)?([^:@\s]+@[^:@\s]+)$')

    def __init__(self):
        self.smtp = SMTP(config.email['smtp_server'])
        context = ssl.create_default_context()
        self.smtp.starttls(context=context)
        self.smtp.ehlo()
        self.smtp.login(config.email['smtp_username'], config.email['smtp_password'])

    def notify(self, contact, node):
        receipient = self.regex.match(contact).group(1)
        msg = MIMEText(node.format_infotext(config.email['text']), _charset='utf-8')
        msg['Subject'] = '[Nodewatcher] %s offline' % node.name
        msg['From'] = config.email['from']
        msg['To'] = receipient

        self.smtp.send_message(msg)
        return True

    def quit(self):
        self.smtp.quit()

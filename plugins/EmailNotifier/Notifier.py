import re
import ssl
from smtplib import SMTP
from email.mime.text import MIMEText
from time import time
from BaseNotifier import BaseNotifier


class EmailNotifier(BaseNotifier):
    regex = re.compile('^(?:mailto:)?([^:@\s]+@[^:@\s]+)$')

    def __init__(self, config):
        self.config = config
        self.smtp = SMTP(config['smtp_server'])
        context = ssl.create_default_context()
        context.check_hostname=False
        context.verify_mode=ssl.CERT_NONE
        self.smtp.starttls(context=context)
        self.smtp.ehlo()
        self.smtp.login(
            self.config['smtp_username'],
            self.config['smtp_password']
        )

    def notify(self, contact, node):
        receipient = self.regex.match(contact).group(1)
        msg = MIMEText(
            node.format_infotext(self.config['text']),
            _charset='utf-8'
        )
        msg['Subject'] = '[Nodewatcher] %s offline' % node.name
        msg['From'] = self.config['from']
        msg['To'] = receipient

        self.smtp.send_message(msg)
        return True

    def quit(self):
        self.smtp.quit()

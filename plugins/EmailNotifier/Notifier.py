import re
import ssl
from smtplib import SMTP, SSLFakeFile, _have_ssl
from email.mime.text import MIMEText
from time import time
from BaseNotifier import BaseNotifier
import config

class MySMTP(SMTP):
    def connect(self, host, port):
        self.host = host
        return super().connect(host, port)

    def starttls(self, keyfile=None, certfile=None):
        """Puts the connection to the SMTP server into TLS mode.

        If there has been no previous EHLO or HELO command this session, this
        method tries ESMTP EHLO first.

        If the server supports TLS, this will encrypt the rest of the SMTP
        session. If you provide the keyfile and certfile parameters,
        the identity of the SMTP server and client can be checked. This,
        however, depends on whether the socket module really checks the
        certificates.

        This method may raise the following exceptions:

         SMTPHeloError            The server didn't reply properly to
                                  the helo greeting.
        """
        self.ehlo_or_helo_if_needed()
        if not self.has_extn("starttls"):
            raise SMTPException("STARTTLS extension not supported by server.")
        (resp, reply) = self.docmd("STARTTLS")
        if resp == 220:
            if not _have_ssl:
                raise RuntimeError("No SSL support included in this Python")
            self.sock = ssl.wrap_socket(self.sock, keyfile, certfile, ca_certs=config.ca_certs, cert_reqs=ssl.CERT_REQUIRED)
            cert = self.sock.getpeercert()
            ssl.match_hostname(cert, self.host)
            self.file = SSLFakeFile(self.sock)
            # RFC 3207:
            # The client MUST discard any knowledge obtained from
            # the server, such as the list of SMTP service extensions,
            # which was not obtained from the TLS negotiation itself.
            self.helo_resp = None
            self.ehlo_resp = None
            self.esmtp_features = {}
            self.does_esmtp = 0
        return (resp, reply)

class EmailNotifier(BaseNotifier):
    regex = re.compile('^(?:mailto:)?([^:@\s]+@[^:@\s]+)$')

    def __init__(self):
        self.smtp = MySMTP(config.email['smtp_server'])
        self.smtp.ehlo()
        if self.smtp.has_extn('STARTTLS'):
            self.smtp.starttls()
        self.smtp.login(config.email['smtp_username'], config.email['smtp_password'])

    def notify(self, contact, node):
        receipient = self.regex.match(contact).group(1)
        msg = MIMEText(config.notify_text_long % {
            'mac': node.mac,
            'name': node.name,
            'contact': receipient,
            'since': str(int((time() - node.lastseen) / 60)) + 'm',
        }, _charset='utf-8')
        msg['Subject'] = '[Nodewatcher] %s offline' % node.name
        msg['From'] = config.email['from']
        msg['To'] = receipient

        self.smtp.send_message(msg)
        return True

    def quit(self):
        self.smtp.quit()

import re
from time import sleep
from sleekxmpp import ClientXMPP
from BaseNotifier import BaseNotifier

class XMPPNotifier(BaseNotifier):
    regex = re.compile('^xmpp:([^:@\s]+@[^:@\s]+)$')

    def __init__(self, config):
        self.config = config
        self.started = False
        self.xmpp = ClientXMPP(self.config['username'], self.config['password'])
        self.xmpp.add_event_handler('session_start', self.start)
        self.xmpp.connect(address=self.config['server'], use_tls=True)
        self.xmpp.process()

    def start(self, event):
        self.xmpp.send_presence()
        self.xmpp.get_roster()
        self.started = True

    def notify(self, contact, node):
        msg = node.format_infotext(self.config['text'])
        receipient = self.regex.match(contact).group(1)

        self.xmpp.send_message(mto=receipient, mbody=msg, mtype='chat')
        return True

    def quit(self):
        while not self.started:
            sleep(0.5)
        self.xmpp.disconnect(wait=True)

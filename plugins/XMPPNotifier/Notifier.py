import re
from sleekxmpp import ClientXMPP
from BaseNotifier import BaseNotifier
import config

class XMPPNotifier(BaseNotifier):
    regex = re.compile('^xmpp:([^:@\s]+@[^:@\s]+)$')

    def __init__(self):
        self.xmpp = ClientXMPP(config.xmpp['username'], config.xmpp['password'])
        self.xmpp.add_event_handler('session_start', self.start)
        self.xmpp.connect(address=config.xmpp['server'], use_tls=True)
        self.xmpp.process()

    def start(self, event):
        self.xmpp.send_presence()
        self.xmpp.get_roster()

    def notify(self, contact, node):
        msg = config.notify_text_short % {
            'mac': node.mac,
            'name': node.name,
            'contact': contact,
            'since': str(int((time() - node.lastseen) / 60)) + 'm',
        }
        receipient = self.regex.match(contact).group(1)

        self.xmpp.send_message(mto=receipient, mbody=msg, mtype='chat')
        return True

    def quit(self):
        self.xmpp.disconnect(wait=True)

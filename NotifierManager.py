import sys
import os
import imp
import config
from time import time
from sqlalchemy import or_
from PluginManager import PluginManager
from db import session, Node

class NotifierManager(PluginManager):
    modulename = 'Notifier'

    def find_matching(self, contact):
        for notifier in self.plugins:
            try:
                if notifier.suitable(contact):
                    return notifier
            except:
                sys.excepthook(*sys.exc_info())

    def notify_node(self, node):
        notifier = self.find_matching(node.contact)
        if notifier:
            return notifier.notify(node)
        else:
            return False

    def notify_down(self):
        to_notify = session.query(Node).filter(
            Node.lastseen <= time() - config.notify_timeout,
            or_(Node.lastcontact < Node.lastseen, Node.lastcontact == None),
            Node.contact != None,
        )
        for node in to_notify:
            if input('Notify for %s via %s? ' % (node.name, node.contact)) != 'y':
                continue
            if self.notify_node(node):
                node.lastcontact = time()
        session.commit()

if __name__ == '__main__':
    m = NotifierManager()
    print("Available notifiers:")
    for notifier in m.plugins:
        print("%s\t%s" % (notifier.__class__.__name__, notifier.regex.pattern))
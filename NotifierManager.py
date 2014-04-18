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

    @staticmethod
    def split_contacts(contacts):
        try:
            return contacts.split(', ')
        except AttributeError:
            return [contacts]

    def notify_node(self, node):
        contacts = self.split_contacts(node.contact)
        copy_contacts = self.split_contacts(config.copy_contact)

        notified = False
        for contact in contacts:
            notifier = self.find_matching(contact)
            if notifier:
                notified |= bool(notifier.notify(contact, node))

        for contact in set(copy_contacts) - set(contacts):
            notifier = self.find_matching(contact)
            if notifier:
                notifier.notify(contact, node)

        return notified

    def notify_down(self):
        to_notify = session.query(Node).filter(
            Node.lastseen <= time() - config.notify_timeout,
            or_(Node.lastcontact < Node.lastseen, Node.lastcontact == None),
            Node.contact != None,
            Node.ignore.in_([None, 0]),
        )
        for node in to_notify:
            if self.notify_node(node):
                node.lastcontact = time()
        session.commit()

if __name__ == '__main__':
    m = NotifierManager()
    print("Available notifiers:")
    for notifier in m.plugins:
        print("%s\t%s" % (notifier.__class__.__name__, notifier.regex.pattern))

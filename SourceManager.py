import sys
import os
import imp
import config
from time import time
from PluginManager import PluginManager
from db import session, Node

class SourceManager(PluginManager):
    modulename = 'Source'

    def get_nodes(self):
        nodes = []
        for notifier in self.plugins:
            try:
                nodes.extend(notifier.nodes())
            except:
                sys.excepthook(*sys.exc_info())
        return nodes

    def update_database(self):
        nodes = self.get_nodes()
        for node in nodes:
            dbnode = session.query(Node).filter_by(mac=node['mac']).first()
            if not dbnode:
                dbnode = Node(**node)
                session.add(dbnode)
            if node['online']:
                dbnode.lastseen = time()
        session.commit()

if __name__ == '__main__':
    m = SourceManager()
    print("Available sources:")
    for source in m.plugins:
        print("%s" % source.__class__.__name__)

import sys
import os
import logging
import config
from time import time
from PluginManager import PluginManager
from db import session, Node

logger = logging.getLogger(__name__)

class SourceManager(PluginManager):
    modulename = 'Source'

    def get_nodes(self):
        nodes = []
        # TODO: detect duplicates
        for source in self.plugins:
            try:
                nodes.extend(source.nodes())
            except:
                logger.exception("Exception while getting nodes from %s" % source.__class__.__name__)
                # If a source failed, we do not want to massively report
                # false-positives, thus re-raise the exception here!
                raise
        return nodes

    def update_database(self):
        nodes = self.get_nodes()
        for node in nodes:
            dbnode = session.query(Node).filter_by(id=node['id']).first()
            if not dbnode:
                dbnode = Node(id=node['id'])
                session.add(dbnode)
            dbnode.name = node['name']
            dbnode.contact = node.get('contact')
            if node.get('lastseen'):
                dbnode.lastseen = node['lastseen']
            elif node['online']:
                dbnode.lastseen = time()
        session.commit()

if __name__ == '__main__':
    m = SourceManager()
    print("Available sources:")
    for source in m.plugins:
        print("%s" % source.__class__.__name__)

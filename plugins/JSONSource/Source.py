import json
import codecs
from datetime import datetime
from urllib.request import urlopen

import config


class JSONSource:
    def __init__(self, config):
        self.config = config

    def nodes(self):
        response = urlopen(self.config['url'])
        reader = codecs.getreader('utf-8')
        nodes = json.load(reader(response))['nodes']
        try:
            it = nodes.values()
        except AttributeError:
            it = iter(nodes)
        for node in it:
            try:
                nodeinfo = node['nodeinfo']
                yield {
                    'id': nodeinfo['node_id'],
                    'name': nodeinfo.get('hostname'),
                    'contact': nodeinfo['owner']['contact'],
                    'online': node.get('flags', {}).get('online'),
                    'lastseen': 'lastseen' in node and
                                datetime.strptime(
                                    node['lastseen'] + "+0000",
                                    '%Y-%m-%dT%H:%M:%S%z'
                                ).timestamp()
                }
            except KeyError:
                pass

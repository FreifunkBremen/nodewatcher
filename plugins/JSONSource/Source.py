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
            nodeinfo = node.get('nodeinfo', {})
            yield {
                'mac': nodeinfo.get('network', {}).get('mac'),
                'name': nodeinfo.get('hostname'),
                'contact': nodeinfo.get('owner', {}).get('contact'),
                'online': node.get('flags', {}).get('online'),
                'lastseen': 'lastseen' in node and datetime.strptime(node['lastseen'], '%Y-%m-%dT%H:%M:%S')
            }

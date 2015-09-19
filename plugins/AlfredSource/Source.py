#!/usr/bin/env python3
import subprocess
import json

class AlfredSource:
    def __init__(self, config):
        self.request_data_type = config['request_data_type']

    def nodes(self):
        output = subprocess.check_output(["alfred-json","-z","-r",str(self.request_data_type),"-f","json"])
        alfred_data = json.loads(output.decode("utf-8"))
        nodes = []
        for mac, values in alfred_data.values():
            try:
                yield {
                    'id': values.get('node_id', mac.replace(':', '')),
                    'name': values.get('hostname'),
                    'contact': values['owner']['contact'],
                    'online': 1,
                }
            except KeyError:
                pass

if __name__ == "__main__":
    ad = Alfred()
    al = ad.nodes()
    print(al)

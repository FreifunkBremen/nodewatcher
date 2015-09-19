import re
import logging
import threading
from time import sleep
from queue import Queue, Empty
import irc.client
from BaseNotifier import BaseNotifier

logger = logging.getLogger(__name__)


class ThreadDoneException(Exception):
    pass


class ThreadedIRCClient(threading.Thread):
    def __init__(self, config):
        self.config = config
        super().__init__()
        self.client = irc.client.IRC()
        self.client.add_global_handler("welcome", self.on_connect)
        self.client.add_global_handler("disconnect", self.on_disconnect)
        self.servers = {}

    def privmsg(self, hostname, target, message, port=6667):
        server = self.servers.get(hostname)
        if not server:
            server = self.client.server().connect(
                hostname,
                port,
                self.config['nickname']
            )
            server.welcome = False
            server.queue = Queue()
            self.servers[hostname] = server
            if not self.is_alive():
                self.start()

        privmsg = (target, message)
        server.queue.put(privmsg)

    def on_connect(self, server, event):
        server.welcome = True

    def on_disconnect(self, server, event):
        for k, v in self.servers.items():
            if v == server:
                del self.servers[k]
                break
        logger.debug("Remaining servers: %i" % len(self.servers))
        if not self.servers:
            raise ThreadDoneException()

    def run(self):
        logger.debug("Main IRCNotifier thread running")
        try:
            while True:
                self.client.process_once()
                for server in self.client.connections:
                    if server.welcome:
                        try:
                            while True:
                                privmsg = server.queue.get_nowait()
                                if privmsg == 'QUIT':
                                    server.queue.task_done()
                                    server.disconnect()
                                else:
                                    if privmsg[0][0] == '#':
                                        server.join(privmsg[0])
                                        server.privmsg(*privmsg)
                                        server.part(privmsg[0])
                                    else:
                                        server.privmsg(*privmsg)
                                server.queue.task_done()
                        except Empty:
                            pass
                sleep(0.5)
        except ThreadDoneException:
            pass
        logger.debug("Main IRCNotifier thread ended")

    def quit(self):
        for server in self.client.connections:
            server.queue.put('QUIT')
            server.queue.join()


class IRCNotifier(BaseNotifier):
    regex = re.compile(
        r"""^
            irc://                      # protocol "irc://"
            (?P<server>[a-zA-Z0-9\.]+)  # server
            (?::(?P<port>\d+))?         # optional port ":1234"
            /(?:
                \#?(?P<channel>[^ ,]+)  # channel name, with or without #
            |
                (?P<nick>[^ ,]+),isnick # nickname with ,isnick suffix
            )
            $
        """,
        re.X
    )

    def __init__(self, config):
        self.client = ThreadedIRCClient(config)

    def notify(self, contact, node):
        msg = node.format_infotext(self.config['text'])

        match = self.regex.match(contact)
        if match.group('nick'):
            target = match.group('nick')
        elif match.group('channel'):
            target = '#' + match.group('channel')
        self.client.privmsg(
            match.group('server'),
            target,
            msg,
            match.group('port') or 6667
        )
        return True

    def quit(self):
        self.client.quit()

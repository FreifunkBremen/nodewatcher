class BaseNotifier(object):
    regex = '^$'

    def __init__(self):
        pass

    def notify(self, node):
        raise NotImplementedError()

    def suitable(self, contact):
        return self.regex.match(contact)

import sys
import os
import imp
import logging
import config

logger = logging.getLogger(__name__)

class PluginManager(object):
    modulename = None

    def __init__(self):
        self.plugins = []
        if not self.modulename:
            raise NotImplementedError("%s.modulename not set!" % self.__class__.__name__)
        possibleplugins = os.listdir('plugins')
        for i in possibleplugins:
            location = os.path.join('plugins', i)
            if not os.path.isdir(location):
                continue
            try:
                info = imp.find_module(self.modulename, [location])
            except ImportError:
                continue
            module = imp.load_module(self.modulename, *info)
            try:
                cls = getattr(module, i)
            except AttributeError:
                continue
            finally:
                if info[0]:
                    info[0].close()
            if cls:
                # TODO: instantiate on demand
                try:
                    self.plugins.append(cls())
                except:
                    logger.exception("Exception while instiating %s" % cls.__name__)

    def quit(self):
        for notifier in self.plugins:
            if hasattr(notifier, 'quit'):
                try:
                    notifier.quit()
                except TypeError:
                    pass

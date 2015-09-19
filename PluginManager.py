import sys
import os
import imp
import logging
import config

logger = logging.getLogger(__name__)


class PluginManager(object):
    modulename = None

    def __init__(self, plugins):
        self.plugins = []
        if not self.modulename:
            raise NotImplementedError(
                "%s.modulename not set!",
                self.__class__.__name__
            )
        for plugin in plugins:
            location = os.path.join('plugins', plugin[0])
            if not os.path.isdir(location):
                logger.error("Plugin %s not found", plugin[0])
                continue
            try:
                info = imp.find_module(self.modulename, [location])
            except ImportError:
                logger.exception(
                    "Exception while importing plugin %s",
                    plugin[0]
                )
                continue

            module = imp.load_module(self.modulename, *info)
            try:
                cls = getattr(module, plugin[0])
            except AttributeError:
                logger.error(
                    "Plugin %s has not class to load",
                    plugin[0],
                    self.modulename
                )
                continue
            finally:
                if info[0]:
                    info[0].close()
            if cls:
                # TODO: instantiate on demand
                try:
                    self.plugins.append(cls(plugin[1]))
                except:
                    logger.exception(
                        "Exception while instiating %s",
                        cls.__name__
                    )

    def quit(self):
        for notifier in self.plugins:
            if hasattr(notifier, 'quit'):
                try:
                    notifier.quit()
                except TypeError:
                    pass

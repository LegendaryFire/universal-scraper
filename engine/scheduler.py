import threading
import time

from engine.loader import Loader

class InvalidModuleOrderError(Exception):
    pass

class Scheduler:
    def _instantiate_module(self, module):
        instance = module()
        self._instances.append(instance)
        return instance

    def _instantiate_notifiers(self):
        for notifier in self._loader.get_notifiers():
            notifier.instance = notifier.cls(**notifier.config)

    def _instantiate_plugins(self):
        for notifier in self._loader.get_notifiers():
            if not isinstance(notifier.instance, notifier.cls):
                raise InvalidModuleOrderError("All notifiers must be instantiated before instantiating plugins")

        for plugin in self._loader.get_plugins():
            if 'notifier' in plugin.config:
                notifier = self._loader.get_notifier_by_name(plugin.config['notifier'])
                plugin.config['notifier'] = notifier.instance
            plugin.instance = plugin.cls(**plugin.config)

    def __init__(self, loader: Loader) -> None:
        self._loader = loader
        self._instances = []
        self._threads = []
        self._instantiate_notifiers()
        self._instantiate_plugins()

    def loop_forever(self):
        for module in self._loader.get_plugins():
            thread = threading.Thread(target=module.instance.run)
            self._threads.append(thread)
            thread.start()

    def stop(self):
        for module in self._loader.get_plugins():
            module.instance.stop()

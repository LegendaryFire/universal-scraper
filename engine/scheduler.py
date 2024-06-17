import threading
import time

class Scheduler:
    def _instantiate_module(self, module):
        instance = module()
        self._instances.append(instance)
        return instance

    def __init__(self, modules) -> None:
        self._modules = modules
        self._instances = []
        self._threads = []
        for module in modules:
            instance = self._instantiate_module(module)
            thread = threading.Thread(target=instance.run)
            self._threads.append(thread)
            thread.start()
        time.sleep(5)
        for instance in self._instances:
            instance.stop()
        time.sleep(5)


import time
from engine.plugin import Plugin


class Example(Plugin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._notifier = kwargs.get('notifier', None)

    def parse(self, object):
        pass

    def task(self):
        print("I'm one module!")
        time.sleep(0.3)

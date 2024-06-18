from engine.plugin import Plugin


class Example(Plugin):
    def __init__(self, **kwargs):
        super().__init__()
        self._notifier = kwargs['notifier']

    def parse(self, object):
        pass

from engine.plugin import Plugin


class Craigslist(Plugin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._notifier = kwargs.get('notifier', None)

    def parse(self, object):
        pass

    def task(self):
        pass

from engine.notifier import Notifier


class Example(Notifier):
    def __init__(self):
        super().__init__()
        print("An instance of the example module has been created.")

    def parse(self, object):
        pass

    def run(self):
        pass

from engine.notifier import Notifier


class Example(Notifier):
    def __init__(self):
        print("An instance of the example module has been created.")
        super().__init__()

from engine.plugin import Plugin


class Example(Plugin):
    def __init__(self):
        print("An instance of the example module has been created.")
        super().__init__()
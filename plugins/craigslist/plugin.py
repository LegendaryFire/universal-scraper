from engine.plugin import Plugin


class Craigslist(Plugin):
    def __init__(self):
        super().__init__()
        print("An instance of the craigslist module has been created.")

    def parse(self, object):
        pass

    def run(self):
        pass

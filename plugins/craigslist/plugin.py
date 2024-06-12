from engine.plugin import Plugin


class Craigslist(Plugin):
    def __init__(self):
        print("An instance of the craigslist module has been created.")
        super().__init__()
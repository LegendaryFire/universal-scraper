from importlib import util
from pathlib import Path

class PluginLoader():
    def __discover_plugins(self):
        path = Path("../plugins")
        for dir in [x for x in path.iterdir() if x.is_dir()]:
            breakpoint()

    def __init__(self):
        self.__discover_plugins()


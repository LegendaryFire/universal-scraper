import sys
from importlib import util, import_module
from pathlib import Path
from dataclasses import dataclass

@dataclass
class EntryPoint:
    name: str
    script: Path

class PluginLoader():
    def __discover_plugins(self) -> list[EntryPoint]:
        """Scans the plugins directory and finds the entrypoint to each plugin."""
        results = []
        path = Path("./plugins")
        for dir in [x for x in path.iterdir() if x.is_dir()]:
            script = dir.joinpath("plugin.py")
            if script.is_file():
                results.append(EntryPoint(name=dir.name, script=script))
        return results

    def __init__(self):
        entrypoints = self.__discover_plugins()
        for entrypoint in entrypoints:
            module = self.__load_module(entrypoint)
            example = module.Example()

    def __load_module(self, entrypoint: EntryPoint):
        """Dynamically loads a module given its EntryPoint."""
        spec = util.spec_from_file_location(entrypoint.name, entrypoint.script)
        module = util.module_from_spec(spec)
        sys.modules[module.__name__] = module
        spec.loader.exec_module(module)
        print(f"Module '{module.__name__}' has been loaded successfully.")
        return module

    def get_modules():
        pass

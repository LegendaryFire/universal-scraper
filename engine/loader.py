import sys
from importlib import util
from pathlib import Path
import logging
import yaml
from dataclasses import dataclass
from engine.plugin import Plugin, Notifier


log = logging.getLogger(__name__)


class UnknownModuleTypeError(Exception):
    pass


@dataclass
class EntryPoint:
    name: str
    script: Path


class Loader():
    def _load_config(self):
        """Loads the configuration file."""
        with open('config.yml', 'r') as file:
            self._config = yaml.safe_load(file)

    def _discover_modules(self) -> list[EntryPoint]:
        """Scans the modules directory and finds the entrypoint to each plugin."""
        results = []
        path = Path("./modules")
        for dir in [x for x in path.iterdir() if x.is_dir()]:
            script = dir.joinpath("plugin.py")
            if script.is_file():
                results.append(EntryPoint(name=dir.name, script=script))
        return results

    def _load_module(self, entrypoint: EntryPoint):
        """Dynamically loads a module given its EntryPoint."""
        spec = util.spec_from_file_location(entrypoint.name, entrypoint.script)
        module = util.module_from_spec(spec)
        sys.modules[module.__name__] = module
        spec.loader.exec_module(module)
        log.info(f"Module {module.__name__} loaded successfully")
        return module

    
    def _sort_modules(self, entrypoints: list[EntryPoint]):
        """Sorts modules into their appropriate category."""
        for entrypoint in entrypoints:
            module = self._load_module(entrypoint)
            object_module = getattr(module, module.__name__.capitalize())
            if issubclass(object_module, Plugin):
                self._plugins.append(object_module)
            elif issubclass(object_module, Notifier):
                self._notifiers.append(object_module)
            else:
                raise UnknownModuleTypeError(f"Unable to determine module type of {module.__name__.capitalize()}")

    
    def __init__(self):
        self._config = None
        self._plugins = []
        self._notifiers = []
        entrypoints = self._discover_modules()
        self._sort_modules(entrypoints)


    def get_plugins(self):
        """Returns a list of all loaded plugin modules."""
        return self._plugins
    
    def get_notifiers(self):
        """Returns a list of all loaded notifier modules."""
        return self._notifiers
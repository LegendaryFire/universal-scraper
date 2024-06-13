import sys
from importlib import util
from pathlib import Path
from dataclasses import dataclass
from engine.plugin import Plugin
from engine.notifier import Notifier
import logging

logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


class UnknownModuleTypeError(Exception):
    pass


@dataclass
class EntryPoint:
    name: str
    script: Path


class Loader():
    def _discover_plugins(self) -> list[EntryPoint]:
        """Scans the plugins directory and finds the entrypoint to each plugin."""
        results = []
        path = Path("./plugins")
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

    def __init__(self):
        self._plugins = []
        self._notifiers = []
        entrypoints = self._discover_plugins()
        for entrypoint in entrypoints:
            module = self._load_module(entrypoint)
            object_module = getattr(module, module.__name__.capitalize())
            if issubclass(object_module, Plugin):
                self._plugins.append(object_module)
            elif issubclass(object_module, Notifier):
                self._notifiers.append(object_module)
            else:
                raise UnknownModuleTypeError(f"Unable to determine module type of {module.__name__.capitalize()}")

    def get_plugins(self):
        """Returns a list of all loaded plugin modules."""
        return self._plugins
    
    def get_notifiers(self):
        """Returns a list of all loaded notifier modules."""
        return self._notifiers

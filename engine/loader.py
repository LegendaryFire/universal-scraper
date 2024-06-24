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


class InvalidConfigurationError(Exception):
    pass


@dataclass
class ModuleDef:
    name: str
    script: Path
    cls: object = None
    instance: object = None
    config: dict = None


class Loader():
    def _discover_modules(self) -> list[ModuleDef]:
        """Scans the modules directory and returns a list of module definitions with the name and script path."""
        results = []
        path = Path("./modules")
        for dir in [x for x in path.iterdir() if x.is_dir()]:
            script = dir.joinpath("plugin.py")
            if script.is_file():
                results.append(ModuleDef(name=dir.name, script=script))
        return results

    def _load_module(self, module_def: ModuleDef):
        """Dynamically loads a module given its EntryPoint."""
        spec = util.spec_from_file_location(module_def.name, module_def.script)
        module_type = util.module_from_spec(spec)
        sys.modules[module_type.__name__] = module_type
        spec.loader.exec_module(module_type)
        log.info(f"Module {module_type.__name__} loaded successfully")
        module_def.cls = getattr(module_type, module_type.__name__.capitalize())

    def _load_modules(self):
        for module in self._modules:
            self._load_module(module)

    
    def _sort_modules(self, entrypoints: list[ModuleDef]):
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

    def _load_config(self):
        """Loads the configuration file."""
        with open('config.yml', 'r') as file:
            config = yaml.safe_load(file)

        if 'modules' not in config:
            log.error("Could not find modules in configuration file")
            return

        for module in self._modules:
            if module.name in config['modules']:
                module.config = config['modules'].pop(module.name)
            else:
                log.warning(f'No configuration found for {module.name} module')

        if len(config['modules'].keys()):
            log.warning("Configuration found for non-existant modules")


    def __init__(self):
        self._modules = self._discover_modules()
        self._load_modules()
        self._load_config()


    def get_plugins(self) -> list[ModuleDef]:
        """Returns a list of all loaded plugin modules."""
        plugins = []
        for module in self._modules:
            if issubclass(module.cls, Plugin):
                plugins.append(module)
        return plugins


    def get_notifiers(self) -> list[ModuleDef]:
        """Returns a list of all loaded notifier modules."""
        notifiers = []
        for module in self._modules:
            if issubclass(module.cls, Notifier):
                notifiers.append(module)
        return notifiers


    def get_notifier_by_name(self, name):
        notifiers = self.get_notifiers()
        for notifier in notifiers:
            if notifier.name == name:
                return notifier
        log.warning(f"Module {name} could not be found")
        return None

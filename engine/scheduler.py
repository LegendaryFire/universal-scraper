from celery import Celery

celery = Celery('scheduler', broker='redis://localhost')


class Scheduler:
    def _instantiate_module(self, module):
        instance = module()
        self._instances.append(instance)
        return instance

    def __init__(self, modules) -> None:
        self._modules = modules
        self._instances = []
        for module in modules:
            instance = self._instantiate_module(module)
            celery.task(instance.run, module.__name__)
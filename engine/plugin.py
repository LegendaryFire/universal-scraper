from dataclasses import dataclass
import time
from fake_useragent import UserAgent
import requests
import logging


log = logging.getLogger(__name__)

class Plugin():
    def __init__(self, **kwargs):
        log.info(f"Plugin {self.__class__.__name__.lower()} initialized")
        self._session = requests.Session()
        self._adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self._session.mount('https://', self._adapter)
        self._user_agent = UserAgent().random
        self._running = False
        self._storage = None
        self._notifier = None
        self._run_interval = kwargs.get('run_interval', str())
        self._run_interval = self._run_interval if type(self._run_interval) is int else None

    def request_json(self, url, params=None, headers=None):
        headers = { } if not headers else headers
        headers['User-Agent'] = self._user_agent if 'User-Agent' not in headers else headers['User-Agent']
        resp = self._session.request("get", url, params=params, headers=headers)
        return resp.json()

    def set_storage_engine(self, instance):
        self._storage = instance

    def set_notifier_engine(self, instance):
        self._notifier = instance

    def parse(self, item):
        pass

    def run(self):
        if not self._storage:
            log.warning(f"No storage engine set for {self.__class__.__name__.lower()} plugin.")
        if not self._notifier:
            log.warning(f"No notifier engine set for {self.__class__.__name__.lower()} plugin.")

        self._running = True
        while self._running:
            start_time = time.perf_counter()
            self.task()
            end_time = time.perf_counter()
            duration = end_time - start_time
            if self._run_interval and duration > self._run_interval:
                log.warning(f"Consider increasing run interval, unable to complete task in time by {(duration - self._run_interval):.2f}s")
            elif self._run_interval:
                time_remaining = self._run_interval - duration
                log.info(f"Plugin {self.__class__.__name__.lower()} task finished in {duration:.2f}s, waiting {time_remaining:.2f}s")
                time.sleep(time_remaining)


    def task(self):
        pass
        

    def stop(self):
        self._running = False
        log.info(f"Plugin {self.__class__.__name__.lower()} shutting down")


@dataclass
class Message:
    title: str
    message: str
    image: str | None = None
    extra: dict | None = None
    

class Notifier():
    def __init__(self):
        log.info(f"Notifier {self.__class__.__name__.lower()} initialized")
        self._session = requests.Session()

    def send_notification(self, message: Message) -> bool:
        pass

    @staticmethod
    def parse_message(data) -> Message:
        pass
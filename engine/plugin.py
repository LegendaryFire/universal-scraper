from dataclasses import dataclass
import time
from tkinter import Image
from fake_useragent import UserAgent
import requests
import logging


log = logging.getLogger(__name__)

class Plugin():
    def __init__(self, adapter=None, user_agent=None):
        log.info(f"Module {self.__class__.__name__.lower()} initialized")
        self._session = requests.Session()
        self._adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self._session.mount('https://', (adapter or self._adapter))
        self._user_agent = (user_agent or UserAgent().random)
        self._running = False
        self._storage = None
        self._notifier = None

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
            log.info(f"{self.__class__.__name__} I am running!")
            time.sleep(1)
        

    def stop(self):
        self._running = False
        log.info(f"Module {self.__class__.__name__.lower()} shutting down")


@dataclass
class Message:
    title: str
    message: str
    image: str | None
    extra: dict | None
    

class Notifier():
    def __init__(self):
        self._session = requests.Session()

    def send_notification(self, message: Message, user) -> bool:
        pass

    @staticmethod
    def parse_message(data) -> Message:
        pass
from fake_useragent import UserAgent
import requests


class Plugin():
    def __init__(self, adapter=None, user_agent=None):
        self._session = requests.Session()
        self._adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self._session.mount('https://', (adapter or self._adapter))
        self._user_agent = (user_agent or UserAgent().random)

    def request_json(self, url, params=None, headers=None):
        headers = { } if not headers else headers
        headers['User-Agent'] = self._user_agent if 'User-Agent' not in headers else headers['User-Agent']
        resp = self._session.request("get", url, params=params, headers=headers)
        return resp.json()

    def parse(self, item):
        pass

    def run(self):
        pass

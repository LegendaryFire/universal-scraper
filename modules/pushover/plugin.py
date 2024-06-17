import requests
from engine.plugin import Message, Notifier
import logging

log = logging.getLogger(__name__)

class Pushover(Notifier):
    def __init__(self, **kwargs):
        super().__init__()
        self._session = requests.Session()
        self._token = kwargs['token']
        self._user = kwargs['user']
        self._link = 'https://api.pushover.net/1/messages.json'

    def send_notification(self, message: Message, user) -> bool:
        data = {
            'token': self._token,
            'user': user,
            'title': message.title,
            'message': message.message,
        }
        try:
            files =  {'attachment': ("image.jpg", requests.get(message.image, stream=True).raw, "image/jpeg")} if message.image else { }
            resp = self._session.post(self._link, data=data, files=files)
            resp.raise_for_status()
            log.info(f"{self.__class__} notification sent successfully")
        except requests.RequestException as ex:
            log.warning(f"{self.__class__} unable to send notification, status code {ex.response.status_code}")

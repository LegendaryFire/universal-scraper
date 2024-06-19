import logging
from engine.loader import Loader
from engine.scheduler import Scheduler

logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

if __name__ == "__main__":
    loader = Loader()
    scheduler = Scheduler(loader)
    scheduler.loop_forever()
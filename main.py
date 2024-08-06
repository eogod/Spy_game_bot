from bot import *
import logging
from data import *

class Command:
    help = 'Run bot locally.'

    def __init__(self):
        Base.metadata.create_all(engine)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def handle(self, *args, **options):
        self.logger.info('Starting local bot...')
        bot.polling(none_stop=True)


if __name__ == "__main__":
    command = Command()
    command.handle()

from bot import *
import logging
from data import *
import asyncio

class Command:
    help = 'Run bot locally.'

    def __init__(self):
        Base.metadata.create_all(engine)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def handle(self, *args, **options):
        self.logger.info('Starting local bot...')
        asyncio.run(bot.polling())


if __name__ == "__main__":
    command = Command()
    command.handle()

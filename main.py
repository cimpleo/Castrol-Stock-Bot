import os
import logging.config
from dotenv import load_dotenv
from modules.bot import Bot
from modules.db import DB


def init():
    load_dotenv()
    basepath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    logging.config.fileConfig(os.path.join(basepath, 'logger.conf'))
    logger = logging.getLogger(__name__)
    logger.info('App init complete')


def main():
    db = DB(os.path.join(os.path.dirname(__file__), 'data', 'stock.xlsx'))
    bot = Bot(os.getenv('TELEGRAM_ACCESS_TOKEN'), db)


# Press the green button in the gutter to run the script.
init()
if __name__ == '__main__':
    main()

import os
import logging.handlers
from dotenv import load_dotenv
from bot import Bot
from db import DB


def init():
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    log_filename = os.path.join(os.path.dirname(__file__), 'logfile.log')
    log_handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=1000000, backupCount=5)
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)

    logging.info('App init')


def main():
    db = DB(os.path.join(os.path.dirname(__file__), 'data', 'stock.xlsx'))
    bot = Bot(os.getenv('TELEGRAM_ACCESS_TOKEN'), db)


# Press the green button in the gutter to run the script.
init()
if __name__ == '__main__':
    main()

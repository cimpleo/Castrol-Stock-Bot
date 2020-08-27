from telegram import Update, ParseMode
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
from modules.db import DB


class Bot:
    db: DB
    updater: Updater
    dispatcher: Dispatcher

    def __init__(self, token, db: DB):
        self.db = db

        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_error_handler(self.handler_error)
        self.dispatcher.add_handler(CommandHandler('start', self.handler_start))
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handler_message))

        self.updater.start_polling()
        self.updater.idle()

        logging.info('Telegram bot init complete')

    def handler_error(self, update: Update, context: CallbackContext):
        logging.error('Update "%s" caused error "%s"', update, context)

    def handler_start(self, update: Update, context: CallbackContext):
        update.message.reply_text('Привет!')

    def handler_message(self, update: Update, context: CallbackContext):
        logging.info(f'Message received: {update.message.text}')
        input_message = update.message.text.strip().upper()

        reply_message: str = ''
        if input_message in self.db.data:
            db_record = self.db.data[input_message]
            logging.info(f'Record found: {db_record}')

            reply_message = reply_message + f'*{db_record[0]["name"]}*\n\nОстатки:\n'

            for item in db_record:
                reply_message = reply_message + f'- {item["stock"]}: {item["count"]}\n'
        else:
            reply_message = 'Не найдено записей с указанным SKU'

        update.message.reply_text(reply_message, parse_mode=ParseMode.MARKDOWN)

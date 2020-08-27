from telegram import Update
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
import logging.handlers
from db import DB


class Bot:
    db: DB
    logger: logging.Logger
    updater: Updater
    dispatcher: Dispatcher

    def __init__(self, token, db: DB):
        self.logger = logging.getLogger(__name__)
        self.db = db

        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_error_handler(self.handler_error)
        self.dispatcher.add_handler(CommandHandler('start', self.handler_start))
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handler_message))

        self.updater.start_polling()
        self.updater.idle()

    def handler_error(self, update: Update, context: CallbackContext):
        self.logger.error('Update "%s" caused error "%s"', update, context)

    def handler_start(self, update: Update, context: CallbackContext):
        update.message.reply_text('Привет!')

    def handler_message(self, update: Update, context: CallbackContext):
        self.logger.info(f'Message received: {update.message.text}')
        update.message.reply_text(self.db.data[update.message.text])

import logging
import traceback
from telegram import Update
from telegram.ext import Updater, CallbackContext


class ReviewerBot:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    def __init__(self, bot_token, chat_id):
        self.updater = Updater(bot_token)
        self.chat_id = chat_id
        self.dispatcher = self.updater.dispatcher
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.dispatcher.add_error_handler(self.error_handler)

        self.updater.start_polling()
        self.send_message('Бот стартовал')
        self.updater.idle()

    def error_handler(self, update: Update, context: CallbackContext):
        self.logger.error(msg="Exception while handling an update:", exc_info=context.error)
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        message = tb_list[-1]
        context.bot.send_message(chat_id=self.chat_id, text=message)

    def send_message(self, message):
        self.updater.bot.send_message(chat_id=self.chat_id, text=message)


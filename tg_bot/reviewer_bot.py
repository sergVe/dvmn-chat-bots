import logging
import traceback
from telegram import Update
from telegram.ext import Updater, CallbackContext
from dvmn_api.dvmn_api import DevmanAPI
from textwrap import dedent
import requests
from utils.logging_util import get_error_msg


class ReviewerBot:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    def __init__(self, bot_token, chat_id):
        self.updater = Updater(bot_token)
        self.chat_id = chat_id
        self.dispatcher = self.updater.dispatcher
        self.logger = logging.getLogger(__name__)
        self.api = DevmanAPI()

    def run(self):
        self.dispatcher.add_error_handler(self.error_handler)
        self.send_message('Бот стартовал')

        self.updater.start_polling()
        while True:
            try:
                self.api.execute()
                if self.api.review_msg:
                    self.send_message(dedent(self.api.review_msg))
                    self.api.review_msg = None

            except (ZeroDivisionError,
                    requests.exceptions.HTTPError,
                    requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectionError
                    ) as e:
                self.send_message('Бот упал с ошибкой')
                self.send_message(dedent(get_error_msg(e)))
                print(get_error_msg(e))
                if isinstance(e, (ZeroDivisionError, requests.exceptions.HTTPError)):
                    break

        self.updater.idle()

    def error_handler(self, update: Update, context: CallbackContext):
        self.logger.error(msg="Exception while handling an update:", exc_info=context.error)
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        message = tb_list[-1]
        context.bot.send_message(chat_id=self.chat_id, text=message)

    def send_message(self, message):
        self.updater.bot.send_message(chat_id=self.chat_id, text=message)


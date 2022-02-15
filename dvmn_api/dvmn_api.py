import os
import requests
from tg_bot.reviewer_bot import ReviewerBot


class DevmanAPI:
    devman_key = os.environ['DEVMAN_KEY']
    timeout = 100

    def __init__(self):
        self.tg_bot = self.init_bot()
        self.timestamp = None

    def init_bot(self):
        return ReviewerBot(
            bot_token=os.environ['TELEGRAM_KEY'],
            chat_id=os.environ['CHAT_ID']
        )

    def get_code_review(self, devman_key, timestamp):
        url = 'https://dvmn.org/api/long_polling/'
        headers = {
            'Authorization': f'Token {devman_key}'
        }
        query_params = {
            'timestamp': timestamp
        }
        response = requests.get(url, headers=headers, params=query_params, timeout=DevmanAPI.timeout)
        response.raise_for_status()

        return response.json()

    def execute(self):
        server_answer = self.get_code_review(devman_key=DevmanAPI.devman_key, timestamp=self.timestamp)
        # print(server_answer)
        if server_answer['status'] == 'timeout':
            self.timestamp = server_answer.get('timestamp_to_request')

        elif server_answer['status'] == 'found':
            self.timestamp = server_answer.get('last_attempt_timestamp')
            last_review = server_answer['new_attempts'][-1]
            lesson_title = last_review['lesson_title']
            review_answer = 'К сожалению, в работе нашлись ошибки' if last_review['is_negative'] \
                else 'Преподавателю всё понравилось, можете приступать к следующему уроку'
            lesson_url = last_review['lesson_url']
            message_text = f'''\
                У Вас проверили работу "{lesson_title}"
                {review_answer}
                Ссылка на урок: {lesson_url}'''
            self.tg_bot.send_message(message_text)

    def run(self):
        self.tg_bot.run()
        while True:
            try:
                self.execute()
            except requests.exceptions.HTTPError as e:
                print(e)
                return
            except requests.exceptions.ReadTimeout as e:
                print(e)
            except requests.exceptions.ConnectionError as e:
                print(e)

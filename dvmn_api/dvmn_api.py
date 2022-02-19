import os
import requests
from dotenv import load_dotenv  # Эту строчку закомментируйте или удалите для деплоя на Heroku


class DevmanAPI:
    devman_key = os.getenv('DEVMAN_KEY')
    timeout = 100

    def __init__(self):
        self.timestamp = None
        self.review_msg = None
        load_dotenv()  # Эту строчку закомментируйте или удалите для деплоя на Heroku

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
        # a = 1 / 0
        server_answer = self.get_code_review(devman_key=DevmanAPI.devman_key, timestamp=self.timestamp)

        if server_answer['status'] == 'timeout':
            self.timestamp = server_answer.get('timestamp_to_request')

        elif server_answer['status'] == 'found':
            self.timestamp = server_answer.get('last_attempt_timestamp')
            last_review = server_answer['new_attempts'][-1]
            lesson_title = last_review['lesson_title']
            review_answer = 'К сожалению, в работе нашлись ошибки' if last_review['is_negative'] \
                else 'Преподавателю всё понравилось, можете приступать к следующему уроку'
            lesson_url = last_review['lesson_url']

            self.review_msg = f'''\
                У Вас проверили работу "{lesson_title}"
                {review_answer}
                Ссылка на урок: {lesson_url}'''

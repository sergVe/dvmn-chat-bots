import os
import time
import requests
from dotenv import load_dotenv
from textwrap import dedent
from telegram.ext import ExtBot


def get_code_review(devman_key, timestamp):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {devman_key}'
    }
    query_params = {
        'timestamp': timestamp
    }
    response = requests.get(url, headers=headers, params=query_params, timeout=5)
    response.raise_for_status()

    return response.json()


def main():
    load_dotenv()
    timestamp = None
    bot = ExtBot(token=os.getenv('TELEGRAM_KEY'))

    while True:

        try:
            server_answer = get_code_review(devman_key=os.getenv('DEVMAN_KEY'), timestamp=timestamp)
            print(server_answer)
            if server_answer['status'] == 'timeout':
                timestamp = server_answer.get('timestamp_to_request')

            elif server_answer['status'] == 'found':
                timestamp = server_answer.get('last_attempt_timestamp')
                last_review = server_answer['new_attempts'][-1]
                lesson_title = last_review['lesson_title']
                review_answer = 'К сожалению, в работе нашлись ошибки' if last_review['is_negative'] \
                    else 'Преподавателю всё понравилось, можете приступать к следующему уроку'
                lesson_url = last_review['lesson_url']
                message_text = f'''\
                У Вас проверили работу "{lesson_title}"\
                {review_answer}
                Ссылка на урок: {lesson_url}'''

                bot.send_message(chat_id=os.getenv('CHAT_ID'), text=dedent(message_text))

        except requests.exceptions.HTTPError as e:
            print(e)
            break
        except requests.exceptions.ReadTimeout as e:
            print(e)
            time.sleep(180)
        except requests.exceptions.ConnectionError as e:
            print(e)
            time.sleep(600)


if __name__ == '__main__':
    main()

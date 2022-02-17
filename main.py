import os
from dotenv import load_dotenv
from tg_bot.reviewer_bot import ReviewerBot


def main():
    load_dotenv()
    bot = ReviewerBot(os.getenv('TELEGRAM_KEY'), os.getenv('CHAT_ID'))
    bot.run()



if __name__ == '__main__':
    main()
import os

from tg_bot.reviewer_bot import ReviewerBot


def main():
    bot = ReviewerBot(os.environ['TELEGRAM_KEY'], os.environ['CHAT_ID'])
    bot.run()



if __name__ == '__main__':
    main()
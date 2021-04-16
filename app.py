import sys
import os
from application.chat_bot import TwitchBot
from config import config


def main():
    try:
        username = config.T_USERNAME
        print(username)
        print(os.getenv("T_USERNAME"))
        client_id = config.T_CLIENT_ID
        token = config.T_TOKEN
        channel = config.T_CHANNEL

        print(f'User: {username} with client id: {client_id} is logging in as bot.')

        bot = TwitchBot(username, client_id, token, channel)
        bot.run()
    except Exception as err:
        print(err)
        sys.exit(1)


if __name__ == "__main__":
    main()

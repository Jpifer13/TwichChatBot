import os
from unittest.mock import patch, MagicMock
from application.chat_bot import TwitchBot
import pytest
from config import config


@pytest.fixture(scope='session')
def bot():
    username = 'test_username'
    client_id = 'test_client_id'
    token = 'test_token'
    channel = 'test_channel'

    with patch('application.chat_bot.TwitchBot._load_channel_id') as _:
        with patch('application.chat_bot.TwitchBot._load_username_logs') as _:
                bot = TwitchBot(username, client_id, token, channel)
    yield bot


class MockMessage:
    def __init__(self, faker):
        self.arguments = ['!game']
        self.source = faker.name()
        self.tags = [
            {
                'key': 'badge-info',
                'value': None
            },
            {
                'key': 'user-id',
                'value': faker.pystr()
            }
        ]
        self.target = f'#{faker.name()}'
        self.type = 'pubmsg'


class DataGenerator:
    def __init__(self, faker):
        self.fake = faker
    
    def create_message(self):
        e = MockMessage(self.fake)
        c = MagicMock()
        return(e, c)


@pytest.fixture(scope='function')
def generator(faker):
    return DataGenerator(faker)


@pytest.fixture(scope='function')
def configuration():
    return config


class Mock_Bot:
    def __init__(self):
        self.api_client_id = '2352345345'
        self.api_oauth = 'edfg324t'
        self.server = 'irc.chat.twitch.tv'
        self.port = 6667
        self.client_id = 'some_id'
        self.token = 'Bearer token'
        self.channel = '#some_channel'
        self.working_directoy = os.getcwd()
        self.channel_id = None
        self.username = 'Mock_Bot' # TwitchBots username
        self.users = None  # List of all usernames
        self._active = True  # If false commands won't work, to handle overflow of traffic

    def get_insults(self):
        try:
            insult_list = [line.rstrip('\n') for line in open(f'{self.working_directoy}/application/resources/insults.txt')]
            return insult_list
        except (FileNotFoundError, Exception) as err:
            print(err)


@pytest.fixture(scope='session')
def users():
    users = {"plastichardware!plastichardware@plastichardware.tmi.twitch.tv": {
        "comments": 17,
        "tags": [
            {
                "key": "badge-info",
                "value": None
            },
            {
                "key": "badges",
                "value": "moderator/1,premium/1"
            },
            {
                "key": "client-nonce",
                "value": "f474d6974a089bc187eb61e76a5def52"
            },
            {
                "key": "color",
                "value": None
            },
            {
                "key": "display-name",
                "value": "Plastichardware "
            },
            {
                "key": "emotes",
                "value": None
            },
            {
                "key": "flags",
                "value": None
            },
            {
                "key": "id",
                "value": "af8887c2-08b4-46f1-84f8-fa8919697b01"
            },
            {
                "key": "mod",
                "value": "1"
            },
            {
                "key": "room-id",
                "value": "130684441"
            },
            {
                "key": "subscriber",
                "value": "0"
            },
            {
                "key": "tmi-sent-ts",
                "value": "1618545199179"
            },
            {
                "key": "turbo",
                "value": "0"
            },
            {
                "key": "user-id",
                "value": "98517746"
            },
            {
                "key": "user-type",
                "value": "mod"
            }
        ],
        "messages": [
            "teyr",
            "fhj,",
            "!roast",
            "!title",
            "!viewers",
            "!viewers",
            "!viewers",
            "!viewers",
            "!viewers",
            "!viewers",
            "!viewers",
            "boom!",
            "i was in debug mode",
            "try again",
            "!viewers",
            "!viewers",
            "!viewers"
        ]
    }}
    yield users

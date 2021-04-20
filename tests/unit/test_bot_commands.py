from unittest.mock import patch
from application.chat_bot import TwitchBot
from tests.unit.conftest import Mock_Bot


def test_chat_bot_run():
    mock_twitch_bot = Mock_Bot()
    insults = mock_twitch_bot.get_insults()

    assert isinstance(insults, list)


def test_message_creator(generator):
    e, c = generator.create_message()

    assert e.source is not None
    assert isinstance(e.tags, list)
    assert e.target is not None


def test_pub_message(bot, generator, users):
    bot.users = users
    e, c = generator.create_message()
    _ = bot.on_pubmsg(c, e)

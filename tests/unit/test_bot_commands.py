from tests.unit.conftest import Mock_Bot
from unittest.mock import patch


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


def test_pub_message_title(bot, generator, mock_response, users):
    bot.users = users
    e, c = generator.create_message()
    e.arguments = ['!title']
    with patch("requests.get", return_value=mock_response) as _:
        with patch("irc.client.ServerConnection.privmsg", return_value="successful") as _:
            _ = bot.on_pubmsg(c, e)


def test_pub_message_title_line_break_fail(bot, generator, mock_response, users):
    bot.users = users
    e, c = generator.create_message()
    e.arguments = ['!title']
    mock_response.status = mock_response.status + '\n'
    with patch("requests.get", return_value=mock_response) as _:
        with patch("irc.client.ServerConnection.privmsg", return_value="successful") as _:
            _ = bot.on_pubmsg(c, e)

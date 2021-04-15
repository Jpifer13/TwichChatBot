import os
import random
import requests
from irc.bot import SingleServerIRCBot


class TwitchBot(SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = f'#{channel}'

        self.line_list = self.get_insults()

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print(f'Connecting to {server} on port {str(port)}...')
        SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

    def get_insults(self):
        cwd = os.getcwd()
        try:
            insult_list = [line.rstrip('\n') for line in open(f'{cwd}/application/resources/insults.txt')]
            return insult_list
        except (FileNotFoundError, Exception) as err:
            print(err)

    def on_welcome(self, c, e):
        print(f'Joining {self.channel}')

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):

        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print(f'Received command: {cmd}')
            self.do_command(e, cmd)
        else:
            # Log username and possibly send to db
            pass
        return

    def do_command(self, e, cmd):
        c = self.connection

        # Poll the API to get current game.
        if cmd == "game":
            url = f'https://api.twitch.tv/kraken/channels/{self.channel_id}'
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, f'{r["display_name"]} is currently playing {r["game"]}')

        # Poll the API the get the current status of the stream
        elif cmd == "title":
            url = f'https://api.twitch.tv/kraken/channels/{self.channel_id}'
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, f'{r["display_name"]} channel title is currently {r["status"]}')

        # Provide basic information to viewers for specific commands
        elif cmd == "raffle":
            message = "This is an example bot, replace this text with your raffle text."
            c.privmsg(self.channel, message)
        elif cmd == "roast":
            message = random.choice(self.line_list)
            c.privmsg(self.channel, message)

        # The command was not recognized
        else:
            c.privmsg(self.channel, f'Did not understand command: {cmd}')

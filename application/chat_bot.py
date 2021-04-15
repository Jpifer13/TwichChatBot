import os
import random
import logging
import time
import json

from application.utils.LoggingUtils import LoggingUtils

import requests
from irc.bot import SingleServerIRCBot


class TwitchBot(SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel, server='irc.chat.twitch.tv', port=6667, log_level=logging.INFO, console_log_level=None, application='TwitchChatBot'):
        self.log_level = log_level
        self.console_log_level = console_log_level
        self.application = application
        self.logging_utils = None
        self.server = server
        self.port = port
        self.client_id = client_id
        self.token = token
        self.channel = f'#{channel}'
        self.working_directoy = os.getcwd()
        self.channel_id = None
        self.username = username # TwitchBots username
        self.users = None  # List of all usernames

        # Start logger
        self._initialize_logging()
        self.logging_utils.logApplicationStart()
        # Get the channel id, we will need this for v5 API calls
        self._load_channel_id(channel)
        # Create IRC bot connection
        self._load_irc_connection()
        # Load username logs
        self._load_username_logs()
        # Load roasts
        self.line_list = self.get_insults()
    
    def run(self):
        self.start()

    def get_insults(self):
        try:
            insult_list = [line.rstrip('\n') for line in open(f'{self.working_directoy}/application/resources/insults.txt')]
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
        # Log username and if we already have then increase comment value
        source = e.source  # username of the message
        if not self.users.get(source, None):
            # We don't have record of the user so add
            self.users[source] = {'comments': 1, 'tags': e.tags, 'messages': [e.arguments[0]]}
        else:
            # User exists so update records
            self.users[source]['comments'] = self.users[source]['comments'] + 1
            self.users[source]['tags'] = e.tags
            self.users[source]['messages'].append(e.arguments[0])
        
        # Write to json file
        with open(f'{self.working_directoy}/application/utils/usernames.json', 'w') as users:
            json.dump(self.users, users)

        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print(f'Received command: {cmd}')
            self.do_command(e, cmd)
        
        # Update local users json
        self._load_username_logs()
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
    
    def _initialize_logging(self):
        try:
            timestamp = time.strftime("%Y%m%d%H%M%S")
            loggingFile = f'logs/{self.application}-{timestamp}.log'
            self.logging_utils = LoggingUtils(self.application, logFile=loggingFile,
                                        fileLevel=self.log_level, consoleLevel=self.console_log_level)
        except Exception as err:
            print(f"Unable to instantiate logging.\n{err}")
    
    def _load_channel_id(self, channel):
        url = f'https://api.twitch.tv/kraken/users?login={channel}'
        headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']
    
    def _load_irc_connection(self):
        print(f'Connecting to {self.server} on port {str(self.port)}...')
        SingleServerIRCBot.__init__(self, [(self.server, self.port, 'oauth:'+self.token)], self.username, self.username)
    
    def _load_username_logs(self):
        # Open username log
        with open(f'{self.working_directoy}/application/utils/usernames.json') as users:
            self.users = json.load(users)

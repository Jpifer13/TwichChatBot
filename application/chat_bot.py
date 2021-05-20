import os
import random
import logging
import time
import json

from application.utils.LoggingUtils import LoggingUtils

import requests
from irc.bot import SingleServerIRCBot


class TwitchBot(SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel, server='irc.chat.twitch.tv', port=6667,
                 log_level=logging.INFO, console_log_level=None, application='TwitchChatBot', logging_utils=None):
        self.log_level = log_level
        self.console_log_level = console_log_level
        self.application = application
        self.logging_utils = logging_utils
        self.api_client_id = os.getenv('API_CLIENT_ID')
        self.api_oauth = os.getenv('API_OAUTH')
        self.server = server
        self.port = port
        self.client_id = client_id
        self.token = token
        self.channel = f'#{channel}'
        self.working_directoy = os.getcwd()
        self.channel_id = None
        self.username = username  # TwitchBots username
        self.users = None  # List of all usernames
        self._active = True  # If false commands won't work, to handle overflow of traffic

        # Start logger 
        if not self.logging_utils:
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
        self.reactor.scheduler.execute_every(3600, self.timely_reminder)
        self.start()

    def get_insults(self):
        try:
            insult_list = [line.rstrip('\n') for line in open(
                f'{self.working_directoy}/application/resources/insults.txt')]
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

    def timely_reminder(self):
        self.connection.privmsg(
            self.channel,
            "Thanks to all viewers for joining in! If you haven't already, give me a follow! It is greatly appreciated!"
        )

    def on_pubmsg(self, c, e):
        # Log username and if we already have then increase comment value
        source = e.source  # username of the message
        if not self.users:  # username json not found so create
            with open(f'{self.working_directoy}/application/utils/usernames.json', 'w') as users_json:
                json.dump({}, users_json)
        elif self.users:
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
            if self._active:
                self.do_command(e, cmd)
            elif not self._active and cmd == 'activate':
                self.do_command(e, cmd)

        # Update local users json
        self._load_username_logs()

    def do_command(self, e, cmd):
        c = self.connection

        try:
            # Activate and deactivate command
            if cmd == "deactivate":
                self._active = False
                message = 'Ouch! That one hurt my bobblesack... Good luck trying to find me you bastard!'
                c.privmsg(self.channel, message)
            
            
            if cmd == "activate":
                self._active = True
                message = 'I see you came to your senses... Wise choice.'
                c.privmsg(self.channel, message)

            # Poll the API to get current game.
            elif cmd == "game":
                url = f'https://api.twitch.tv/kraken/channels/{self.channel_id}'
                headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
                r = requests.get(url, headers=headers).json()
                if r.get('display_name'):
                    c.privmsg(self.channel, f'{r["display_name"]} is currently playing {r["game"]}')

            # Poll the API the get the current status of the stream
            elif cmd == "title":
                url = f'https://api.twitch.tv/kraken/channels/{self.channel_id}'
                headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
                r = requests.get(url, headers=headers).json()
                if r.get('display_name'):
                    status = r["status"]
                    if "\n" in status:
                        status = r["status"].replace("\n", "")
                    c.privmsg(self.channel, f'{r["display_name"]} channel title is currently {status}')

            # Provide basic information to viewers for specific commands
            elif cmd == "viewers":
                url = 'https://api.twitch.tv/helix/streams?user_id=130684441'
                headers = {'Client-ID': self.api_client_id, 'Authorization': self.api_oauth,
                        'Accept': 'application/vnd.twitchtv.v5+json'}
                r = requests.get(url, headers=headers).json()
                if r.get('data'):
                    c.privmsg(
                        self.channel,
                        f"{r['data'][0]['user_name']}'s channel currently has  {r['data'][0]['viewer_count']} viewers!"
                    )
            
            # Commands
            elif cmd == "commands":
                message = 'Current commands available are: "game", "title", "viewers", "roast", "deactivate"'
                c.privmsg(self.channel, message)

            elif cmd == "roast":
                message = random.choice(self.line_list)
                c.privmsg(self.channel, message)

            # The command was not recognized
            else:
                c.privmsg(self.channel, f'Did not understand command: {cmd}')
        except Exception as err:
            print(err)
            raise Exception

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

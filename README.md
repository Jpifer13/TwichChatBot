<h1>Introduction<h1>

This is a basic chat bot designed using python library irc. (You can get with "pip install irc") Simple to run locally as a python application and also has the ability to be ran in a docker container.

<h2>Set these environment variables before running!<h2>

T_USERNAME - This is the username of your bot account
T_CLIENT_ID - This is the client id of your bot account
T_TOKEN - This is the oauth token your bot needs to be able to connect to the channel chat
T_CHANNEL - This is what channel you wish the bot to connect to
API_CLIENT_ID - This is the client id of your api creds(can be created here: (https://twitchtokengenerator.com/))
API_OAUTH - This is the oath token receive for the api, this will always start with Bearer

<h2>Running locally<h2>

To run locally it very simple and only requires that you have a the few environment variables set from above. The entrypoint to this application is ./app.py.

The first step is to create a virtual environment using your choice of method depending on operating system or virtual environment package. For Python3 and windows navigate to the project folder ./TwitchChatBot/ in a terminal and run:  ```python -m venv venv```  for Linux ```python3 -m venv venv```  This may take a moment as it creates all virtual environment files. Launch the newly create virtual environment with this command:  ```./venv/Scripts/activate```  you will see a "venv" tag to the left of the terminal when activated. Once this is done you need to install all project dependencies, found in requirements.txt. To do so run this command:  ```pip install -r requirements.txt```  or on Linux  ```pip3 install -r requirements.txt```  Now the final step is to run the program!  ```python ./app.py```  and on Linux  ```python3 ./app.py```  

<h2>Running in a docker container<h2>

There is an existing Dockerfile to make this process easy as long as the system you are running this on has docker installed properly. A shell script has been added to build and run the new image as well. So all that needs to be done is create the environment variables above and run deploy.sh. NOTE: Make sure your deploy.sh is executable with this command:  ```chmod 755 deploy.sh```  Then all you have to do is run the script:  ```./deploy.sh```

And that's it! Open up twitch to the channel you selected and try a command in the chat like: "!title"

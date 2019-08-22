# -*- coding: utf-8 -*-
"""
Python Slack Bot class for use with the pythOnBoarding app
"""
import os
import logging
import slack

# To remember which teams have authorized your app and what tokens are
# associated with each team, we can store this information in memory on
# as a global object. When your bot is out of development, it's best to
# save this in a more persistent memory store.
authed_teams = {}

logger = logging.getLogger('gmppostbot.bot')

class Bot(object):
    """ Instantiates a Bot object to handle Slack onboarding interactions."""
    def __init__(self):
        print('CLASS BOT INITIALIZED')
        super(Bot, self).__init__()
        self.name = "pythonboardingbot"
        self.emoji = ":robot_face:"
        # When we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        logger.info("client_id", os.environ.get("client_id"))
        self.oauth = {"client_id": os.environ.get("client_id"),
                      "client_secret": os.environ.get("client_secret"),
                      # Scopes provide and limit permissions to what our app
                      # can access. It's important to use the most restricted
                      # scope that your app will need.
                      "scope": "bot"}
        self.verification = os.environ.get("verification")

        # NOTE: Python-slack requires a client connection to generate
        # an OAuth token. We can connect to the client without authenticating
        # by passing an empty string as a token and then reinstantiating the
        # client with a valid OAuth token once we have one.
        self.client = slack.WebClient(token=os.environ.get("token"))

        # We'll use this dictionary to store the state of each message object.
        # In a production environment you'll likely want to store this more
        # persistently in  a database.

    def auth(self, code):
        print('auth')
        """
        Authenticate with OAuth and assign correct scopes.
        Save a dictionary of authed team information in memory on the bot
        object.

        Parameters
        ----------
        code : str
            temporary authorization code sent by Slack to be exchanged for an
            OAuth token

        """
        # After the user has authorized this app for use in their Slack team,
        # Slack returns a temporary authorization code that we'll exchange for
        # an OAuth token using the oauth.access endpoint
        auth_response = self.client.api_call(
                                "oauth.access",
                                client_id=self.oauth["client_id"],
                                client_secret=self.oauth["client_secret"],
                                code=code
                                )
        # To keep track of authorized teams and their associated OAuth tokens,
        # we will save the team ID and bot tokens to the global
        # authed_teams object
        team_id = auth_response["team_id"]
        logger.info('team_id', team_id)
        authed_teams[team_id] = {"bot_token":
                                 auth_response["bot"]["bot_access_token"]}
        logger.info('authed_teams', authed_teams)
        # Then we'll reconnect to the Slack Client with the correct team's
        # bot token
        self.client = SlackClient(authed_teams[team_id]["bot_token"])

    def onboarding_message(self, slack_event):
        print('onboarding_message')

        try:
            user_id = slack_event["event"]["user"]
            channel = slack_event["event"]["channel"]
            start_onboarding(slack.WebClient(os.environ.get('token')), user_id, channel)
        except:
            print('exception OM')
            pass

    def direct_message(self, slack_event):
        client = slack.WebClient(os.environ.get('token'))

        user = client.users_lookupByEmail(email='rafael9s9@hotmail.com')
        print(user['user']['id'])
        openM = client.im_open(user=user['user']['id'])
        
        #print(user)
        channel = None

        try:
            client.im_history(channel='DMC1A5FDX')
            client.chat_postMessage(channel='DMLJ5150E', text='blablacar do bot')
            client.chat_postMessage(channel='DMC1G9XQR', text='Mensagem do bot')
        except:
            print('exception DM')
            pass


    def start_onboarding(self, web_client, user_id, channel):
        print('onboarding!!!')

        # Post the onboarding message in Slack
        response = web_client.chat_postMessage(
            channel=channel,
            text="It's a onboarding message"
        )

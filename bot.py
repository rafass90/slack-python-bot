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

    def onboarding_message(self):
        print('onboarding_message')
        """Create and send an onboarding welcome message to new users. Save the
        time stamp of this message so we can update this message in the future.
        """
        print(payload)
        # Get the id of the Slack user associated with the incoming event
        user_id = payload["data"]["user"]["id"]
        # Get WebClient so you can communicate back to Slack.
        web_client = payload["web_client"]

        # Open a DM with the new user.
        response = web_client.im_open(user=user_id)
        channel = response["channel"]["id"]

        # Post the onboarding message.
        start_onboarding(web_client, user_id, channel)


    def direct_message(self, slack_event):
        print('message')
        """Create and send an onboarding welcome message to new users. Save the
        time stamp of this message so we can update this message in the future.
        """
        # Get the id of the Slack user associated with the incoming event
        user_id = slack_event["event"]["user"]
        channel = slack_event["event"]["channel"]
        print(user_id)


        # Open a DM with the new user.
        #response = web_client.im_open(user=user_id)
        start_onboarding(web_client, user_id, channel)
        #channel = response["channel"]["id"]

        # Post the onboarding message.
        #start_onboarding(web_client, user_id, channel)

def start_onboarding(web_client: slack.WebClient, user_id: str, channel: str):
    # Get the onboarding message payload
    message = "mensagem teste"

    # Post the onboarding message in Slack
    response = web_client.chat_postMessage(**message)
    onboarding_tutorial.timestamp = response["ts"]

    # Store the message sent in onboarding_tutorials_sent
    if channel not in onboarding_tutorials_sent:
        onboarding_tutorials_sent[channel] = {}
    onboarding_tutorials_sent[channel][user_id] = onboarding_tutorial
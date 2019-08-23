# -*- coding: utf-8 -*-
"""
A routing layer for the onboarding bot tutorial built using
[Slack's Events API](https://api.slack.com/events-api) in Python
"""
import os
import logging
import slack
import ssl as ssl_lib
import certifi


import bot
import os
import logging
from flask import Flask, request, make_response, render_template
import slack
pyBot = bot.Bot()

app = Flask(__name__)
logger = logging.getLogger('gmppostbot')


def _event_handler(event_type, slack_event):
    team_id = slack_event["team_id"]
    print(event_type)
    print('slack_event', slack_event)
    # When the user first joins a team, the type of event will be team_join
    if event_type == "team_join":
        user_id = slack_event["event"]["user"]["id"]
        # Send the onboarding message
        return make_response("Welcome Message Sent", 200,)

    elif event_type == "message":
        pyBot.direct_message(slack_event)
        return make_response("Ok", 200,)


    elif event_type == "member_joined_channel":
        pyBot.onboarding_message(slack_event)
        return make_response("Ok", 200,)

    return make_response(event_type, 200, {"X-Slack-No-Retry": 1})


@app.route("/install", methods=["GET"])
def pre_install():
    print("INSTALL")
    """This route renders the installation page with 'Add to Slack' button."""
    # Since we've set the client ID and scope on our Bot object, we can change
    # them more easily while we're developing our app.
    client_id = pyBot.oauth["client_id"]
    scope = pyBot.oauth["scope"]
    # Our template is using the Jinja templating language to dynamically pass
    # our client id and scope
    return render_template("install.html", client_id=client_id, scope=scope)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    print("THANKS")
    """
    This route is called by Slack after the user installs our app. It will
    exchange the temporary authorization code Slack sends for an OAuth token
    which we'll save on the bot object to use later.
    To let the user know what's happened it will also render a thank you page.
    """
    # Let's grab that temporary authorization code Slack's sent us from
    # the request's parameters.
    code_arg = request.args.get('code')
    # The bot's auth method to handles exchanging the code for an OAuth token
    pyBot.auth(code_arg)
    return render_template("thanks.html")


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = request.get_json()
    print('listening')
    print(slack_event)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                             })
    if pyBot.verification != slack_event.get("challenge"):
        message = "Invalid Slack verification token: %s \npyBot has: \
                   %s\n\n" % (slack_event["token"], pyBot.verification)
        # By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off
        # Slack's automatic retries during development.
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        # Then handle the event by event_type and have your bot respond
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})

if __name__ == '__main__':
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ.get("token")
    app.run(debug=True)

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


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = request.get_json()
    print('listening', slack_event['event']['type'])

    pyBot.close()
    if slack_event['event']['type'] == 'message':
        print('event event', slack_event['event'])
        
        if slack_event['event'].get(key['bot_id', 'd']) != 'd':
            return ''
        if slack_event['event']['user'] == 'UML8H54MD':
            return ''
    pyBot.start_onboarding(slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ.get("token")
    app.run(debug=True)

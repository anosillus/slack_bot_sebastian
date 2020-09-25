# -*- coding: utf-8 -*-
# File name: sebastian.py
# First Edit: 2020-09-22
# Last Change: 2020-09-22

"""
Description

"""

import logging
import os

from slack_bolt import App
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler


logging.basicConfig(level=logging.DEBUG)
bolt_app = App()


@bolt_app.command("/hey-google-app-engine")
def hello(body, ack):
    user_id = body["user_id"]
    ack(f"Hi <@{user_id}>!")


@bolt_app.command("/echo")
def repeat_text(ack, say, command):
    # Acknowledge command request
    ack()
    say(f"{command['text']}")


@bolt_app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hey there <@{message['user']}>!",
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click",
                },
            }
        ],
        text=f"Hey there <@{message['user']}>!",
    )


@bolt_app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)


@app.route("/_ah/warmup")
def warmup():
    # Handle your warmup logic here, e.g. set up a database connection pool

    return "", 200, {}


@app.route("/slack/events", methods=["POST", "GET"])
def slack_events():
    return handler.handle(request)


# Only for local debug

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))

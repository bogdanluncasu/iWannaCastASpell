import os
import sys
import json

import requests
from flask import Flask, request
from aiml import Kernel
from os import listdir
import sys, processing
import time


def set_personality(bot):
    bot.setBotPredicate("name", "Wasluianca")
    bot.setBotPredicate("gender", "robot")
    bot.setBotPredicate("master", "B2Group")
    bot.setBotPredicate("birthday", "21.12.2016")
    bot.setBotPredicate("birthplace", "Iasi")
    bot.setBotPredicate("boyfriend", "you")
    bot.setBotPredicate("favoritebook", "Stories from Vaslui")
    bot.setBotPredicate("favoritecolor", "blue")
    bot.setBotPredicate("favoriteband", "B.U.G Mafia")
    bot.setBotPredicate("favoritesong", "your voice")
    bot.setBotPredicate("forfun", "talktoyou")
    bot.setBotPredicate("friends", "you")
    bot.setBotPredicate("girlfriend", "you")
    bot.setBotPredicate("language", "english")
    bot.setBotPredicate("email", "wasluyanu@bot.ro")


print "Bot initializer"
#bot = Kernel()
#files = sorted(listdir('standard'))
#for file in files:
#    bot.learn('standard/' + file)

#set_personality(bot)
#substs = processing.get_substitutions()

app = Flask(__name__)


def ask_him(data, index, bot, substs, sessionId):
    question = data
    question = processing.apply_substitutions(question, substs)
    reply = bot.respond(question, sessionId)
    return "Bot> " + reply


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "HOLLA", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]["text"]

#                    reply = ask_him(message_text, 0, bot, substs, sender_id)
                    send_message(recipient_id, "JOLLA")

                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("optin"):
                    pass

                if messaging_event.get("postback"):
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


if __name__ == '__main__':
    app.run(debug=True)

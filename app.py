import os
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)


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
	
	#100002478108714
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]  
                    message_text = messaging_event["message"]["text"]  
                    send_message(sender_id, recipient_id)

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


def log(message):
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)

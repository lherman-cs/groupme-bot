from json import load, dumps
from os import chdir
from os.path import dirname

import requests
from flask import Flask, request

import Spider

app = Flask(__name__)

with open("credential.json") as credential:
    CREDENTIAL = load(credential)

SPIDER = Spider()


def reply(name, text):
    url = "https://api.groupme.com/v3/bots/post"

    results = SPIDER.collect(text)
    if results:
        text = "Hey {}, check out these links:\n".format(
            name) + "\n".join(results)
    else:
        text = "I'm sorry {}, I couldn't find what you're looking for."

    data = {
        "bot_id": CREDENTIAL["BOT_ID"],
        "text": text
    }

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post(url, data=dumps(data), headers=headers)
    print(r.status_code)
    print(r.text)


@app.route('/', methods=["POST", ])
def callback():
    error = None
    if request.method == 'POST':
        data = request.get_json()
        name = data["name"]
        text = data["text"].split()

        if len(text) > 1:
            command = text[0].lower()
            sentence = " ".join(text[1:])

            if command == "search":
                reply(name, sentence)


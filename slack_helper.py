from flask import Flask
from flask import request
from flask import jsonify
from flask_mysqldb import MySQL
import logging as logger
import slack
import json
import requests
import MySQLdb

from main import tokens

logger.basicConfig(level="DEBUG")


def post_message(token_id, channel, text):
    url = "https://slack.com/api/chat.postMessage"
    bot_token = tokens['slack_bot_token']
    data = {
        "token": token_id,
        "channel": channel,
        "text": text
    }
    authorization = "Bearer " + bot_token
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization
    }
    json_data = json.dumps(data)
    requests.post(url, data=json_data, headers=headers)

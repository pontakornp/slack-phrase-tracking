from flask import Flask, Blueprint
from flask import request
from flask import jsonify
from flask_mysqldb import MySQL
import logging as logger
import slack
import json
import requests
import MySQLdb

from main import app
from slack_helper import *
from model import *

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * from phrases''')
    results = cur.fetchall()
    logger.debug(results)
    return "Hello, World!"


@app.route('/slack/events', methods=['POST'])
def slack_event():
    if not request.json:
        return {}, 400
    if 'challenge' in request.json:
        data = {
            'challenge': request.json['challenge']
        }
        return data, 200
    req = request.json
    response_dict = {'hey': 'yo'}
    if 'token' in req and 'event' in req:
        token_id = req['token']
        event = req['event']
        if 'type' in event and event['type'] == 'message':
            channel = event['channel']
            text = event['text']
            user_id = event['user']
            if check_phrase_exist(channel, text):
                res_text = "Phrase '"+ text + "' found!"
                post_message(token_id, user_id, res_text)
            else:
                logger.debug("phrase does not exist")
    return {}, 200


@app.route('/slack/addphrase', methods=['POST'])
def slack_addphrase():
    if not request.form:
        return {}, 400
    req = request.form
    if not check_command_fields_exist(req):
        return "", 200
    token_id = req['token']
    user_id = req['user_id']
    if req['command'] == '/addphrase':
        text = req['text']
        channel = req['channel_id']
        channel_name = req['channel_name']
        if not update_phrase(channel, text, user_id):
            return "Phrase is unsuccessfully added, please try again", 200
        msg = "Successfully add phrase '" + text + "' in channel: " + channel_name
        return msg, 200
    return "", 200


@app.route('/slack/deletephrase', methods=['POST'])
def slack_deletephrase():
    if not request.form:
        return {}, 400
    req = request.form
    if not check_command_fields_exist(req):
        return "", 200
    token_id = req['token']
    user_id = req['user_id']
    if req['command'] == '/deletephrase':
        text = req['text']
        channel = req['channel_id']
        channel_name = req['channel_name']
        if not check_phrase_exist(channel, text):
            return "Phrase does not exist, please try again", 200
        if not toggle_phrase(channel, text, False):
            return "Phrase is unsuccessfully deleted, please try again", 200
        msg = "Successfully delete phrase '" + text + "' in channel: " + channel_name
        return msg, 200
    return "", 200


def check_command_fields_exist(req):
    return 'token' in req and 'command' in req and 'user_id' in req

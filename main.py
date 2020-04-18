from flask import Flask
from flask import request
from flask import jsonify
from flask_mysqldb import MySQL
import logging as logger
import slack
import json
import requests
import MySQLdb

logger.basicConfig(level="DEBUG")

tokens = {}
with open('config.json') as json_data:
    tokens = json.load(json_data)

app = Flask(__name__)

from views import *
from model import *

init_db(app, tokens)

if __name__ == '__main__':
    logger.debug("Starting the application")
    app.run()







from flask import Flask
from flask import request
from flask import jsonify
from flask_mysqldb import MySQL
import logging as logger
import slack
import json
import requests
import MySQLdb
import os

logger.basicConfig(level="DEBUG")

tokens = {
    "slack_bot_token": os.environ.get("slack_bot_token"),
    "mysql_host": os.environ.get("mysql_host"),
    "mysql_name": os.environ.get("mysql_name"),
    "mysql_username": os.environ.get("mysql_username"),
    "mysql_password": os.environ.get("mysql_password"),
    "mysql_cursorclass": os.environ.get("mysql_cursorclass")
}

app = Flask(__name__)

from views import *
from model import *

init_db(app, tokens)

if __name__ == '__main__':
    logger.debug("Starting the application")
    app.run()







from flask import Flask
from flask import request
from flask import jsonify
from flask_mysqldb import MySQL
import logging as logger
import slack
import json
import requests
import MySQLdb

from main import app
from main import tokens

logger.basicConfig(level="DEBUG")
mysql = MySQL(app)


def init_db(app, tokens):
    app.config["MYSQL_USER"] = tokens["mysql_username"]
    app.config["MYSQL_PASSWORD"] = tokens["mysql_password"]
    app.config["MYSQL_HOST"] = tokens["mysql_host"]
    app.config["MYSQL_DB"] = tokens["mysql_name"]
    app.config["MYSQL_CURSORCLASS"] = tokens["mysql_cursorclass"]


def update_phrase(channel, text, user_id):
    cur = mysql.connection.cursor()
    sql_command = '''SELECT is_active FROM phrases WHERE channel = "{}" AND text = "{}"'''.format(channel, text)
    logger.debug(sql_command)
    cur.execute(sql_command)
    results = cur.fetchall()
    if len(results) == 1 and results[0]["is_active"]:
        cur.close()
        return True
    elif len(results) == 1 and not results[0]["is_active"]:
        return toggle_phrase(channel, text, True, cur)
    else:
        is_success = True
        sql_command = '''INSERT INTO phrases (channel, text, user_id) VALUES ("{}", "{}", "{}")'''.format(channel, text, user_id)
        try:
            cur.execute(sql_command)
            mysql.connection.commit()
        except MySQLdb.Error:
            is_success = False
        cur.close()
        return is_success


def toggle_phrase(channel, text, is_active, cur=None):
    if cur is None:
        cur = mysql.connection.cursor()
    is_success = True
    try:
        sql_command = '''UPDATE phrases SET is_active = {} WHERE channel = "{}" AND text = "{}"'''.format(is_active, channel, text)
        cur.execute(sql_command)
        mysql.connection.commit()
    except MySQLdb.Error:
        is_success = False
    cur.close()
    return is_success


def check_phrase_exist(channel, text):
    cur = mysql.connection.cursor()
    sql_command = '''SELECT is_active FROM phrases WHERE channel = "{}" AND text = "{}"'''.format(channel, text)
    logger.debug(sql_command)
    cur.execute(sql_command)
    results = cur.fetchall()
    cur.close()
    return len(results) == 1 and results[0]["is_active"]

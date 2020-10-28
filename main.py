# LIBRARY IMPORTS
from flask import Flask, jsonify, request, make_response, redirect, Response
from multiprocessing import Process, Value
from flask_cors import CORS, cross_origin
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path
from time import sleep
from uuid import uuid4

import requests
import telepot
import random
import socket
import json
import time
import os


# FILE IMPORTS
from programs.scheduleBot import bot_class
from programs.sendman import sendman
from programs import portfolio
from config import setConfig

##### FLASK SERVER

app = Flask("API's")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

######## CONFIGS FOR PROGRAMS #########
# Bot for portifolio
setConfig()
bot = telepot.Bot(f"{os.getenv('TELEGRAM_TOKEN')}")
botSchedule = bot_class.Bot()
####### SETUP

# headers for sending
headers = {"Content-Type": "Application/json"}
###########################

#### FOR FLASK FUNCTIONS ####
def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


#############################
#### ROUTES ######
#  DEFAULT ROUTE #
@app.errorhandler(404)
def page_not_found(error):
    return redirect("https://photricity.com/flw/ajax/", code=302)


###############
# Some tests


@cross_origin()
@app.route("/teste", methods=["GET", "POST", "OPTIONS"])
def teste():
    data = {
        "IP": request.remote_addr,
        "body": "Configuration done with success",
    }

    return Response(json.dumps(data), status=200, mimetype="application/json")


##################


@cross_origin()
@app.route("/allw", methods=["GET", "POST", "OPTIONS"])
def register_app_to_notification():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()

    if request.method == "GET":  # CORS preflight
        return jsonify({"Allowed to connect": "200"})

    if request.method == "POST":  # CORS preflight
        return jsonify({"Allowed": "200"})


#  Portifolio routes
@app.route("/portfolio", methods=["POST", "OPTIONS"])
@cross_origin()
def telegram():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        response = portfolio.sendMessageCalderaro(
            request.json["name"],
            request.json["email"],
            request.json["text"],
            bot,
        )
        return response


@app.route("/portfolioHeydrigh", methods=["POST", "OPTIONS"])
@cross_origin()
def telegram():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        response = portfolio.sendMessageHeydrigh(
            request.json["name"],
            request.json["email"],
            request.json["text"],
            bot,
        )
        return response


#### BLOG


#### ECOMP SCHEDULE BOT
@app.route("/schedule_bot", methods=["POST"])
@cross_origin()
def ecompSchedule():
    # handle updates
    print(request.json)
    try:
        msg = request.json["message"]["text"]
        if "show reservations" in msg.lower():
            botSchedule.getSchedulesPresentationList(request.json)
        elif "reservation" in msg.lower():
            botSchedule.handleUpdates(request.json)
    except:
        pass

    return Response("{'ok': true}", status=200, mimetype="application/json")


@app.route("/schedule_bot/verify", methods=["GET"])
@cross_origin()
def botVerifySchedule():
    # handle updates
    botSchedule.verifySchedule()
    return Response('{"ok": true}', status=200, mimetype="application/json")


# Some functions


def botKeepAlive():
    def getTime():
        tm = datetime.now()
        tm = datetime(
            tm.year,
            tm.month,
            tm.day,
            tm.hour - 3,
            tm.minute,
        )
        return tm

    sec = 0
    while True:
        tm = getTime()
        if tm.hour > 8 and tm.hour < 23:
            print(sec / 21600)
            if sec / 21600 == 1:
                print("verify")
                requests.get(
                    "https://felipecalderaroapis.herokuapp.com/schedule_bot/verify"
                )
                sec = 0
            else:
                print("keep alive")
                requests.get("https://felipecalderaroapis.herokuapp.com/allw")
        else:
            sec = 0
            requests.get("https://felipecalderaroapis.herokuapp.com/allw")

        sleep(1200)
        sec += 1200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 34939))
    # Process(target=someFunction, args=(x,)).start()
    # Process(target=botKeepAlive,).start()
    app.run(host=getIp(), port=port, debug=True, threaded=True)
    # app.run(host="0.0.0.0", port=port)
    # last_update()

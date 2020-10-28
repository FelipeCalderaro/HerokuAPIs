from programs.sendman.sendman import chatIds, send
from flask import Response
import requests
import json


def sendMessageCalderaro(name, email, text, bot):
    try:
        message = f"PORTFOLIO\n\nName: {name}\nEmail: {email}\nMessage:\n\n{text}"
        bot.sendMessage(chat_id=chatIds.calderaro, text=message)
        return Response(
            json.dumps(
                {"status": "Message sent successfully"},
            ),
            status=201,
            mimetype="content-type:application/json",
        )
    except Exception as e:
        return Response(
            json.dumps(
                {
                    "error": f"{e}",
                    "status_description": "This response is sent when the web server after performing a server-oriented content negotiation, does not find any content following the criteria provided by the user agent.",
                },
                status=406,
            )
        )


def sendMessageHeydrigh(name, email, text, bot):
    try:
        message = f"PORTFOLIO\n\nName: {name}\nEmail: {email}\nMessage:\n\n{text}"
        bot.sendMessage(chat_id=chatIds.heydrigh, text=message)
        return Response(
            json.dumps(
                {"status": "Message sent successfully"},
            ),
            status=201,
            mimetype="content-type:application/json",
        )
    except Exception as e:
        return Response(
            json.dumps(
                {
                    "error": f"{e}",
                    "status_description": "This response is sent when the web server after performing a server-oriented content negotiation, does not find any content following the criteria provided by the user agent.",
                },
            ),
            status=406,
            mimetype="content-type:application/json",
        )

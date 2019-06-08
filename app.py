from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
#from twilio.rest import Client

from utils import fetch_reply


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST', 'GET'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    #msg = request.form.get('Body')

    print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('From')

    # Create reply
    #resp = MessagingResponse()
    #resp.message("You said: {}".format(msg))

    resp = MessagingResponse()
    msg = resp.message(fetch_reply(msg, sender))
    
    
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
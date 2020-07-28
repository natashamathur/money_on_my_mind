from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
from functions_for_budget_tracker import *

# https://www.twilio.com/blog/2016/09/how-to-receive-and-respond-to-a-text-message-with-python-flask-and-twilio.html
# first run ./ngrok http 5000 in a different tab
# then run this
# put ngrok address in https://www.twilio.com/console/phone-numbers


app = Flask(__name__)


@app.route("/sms", methods=["POST"])
def sms():

    message_body = request.form["Body"]
    if "status" in message_body.lower():
        print("here")
        message = report_card("expenses.json")

    resp = MessagingResponse()

    resp.message(message)
    return str(resp)


if __name__ == "__main__":
    app.run()

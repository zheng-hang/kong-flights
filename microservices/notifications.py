from dotenv import load_dotenv
import os
import threading
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from email.message import EmailMessage
import ssl
import smtplib

import amqp_connection
import json
import pika

#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

app = Flask(__name__)

CORS(app)

# Set env path
dotenv_path = 'vue-frontend/.env'
# Load environment variables from .env file
load_dotenv(dotenv_path)


@app.route("/booking", methods=['POST'])
def receivePaymentData():
    # Check if the booking contains valid JSON
    booking = None
    if request.is_json:
        booking = request.get_json()
        result = processNotification(booking)
        return jsonify(result), result["code"]
    else:
        data = request.get_data()
        print("Received invalid payment data:")
        print(data)
        return jsonify({"code": 400,
                        # make the data string as we dunno what could be the actual format
                        "data": str(data),
                        "message": "Payment data should be in JSON."}), 400  # Bad Request input

def processNotification(booking):
    print("Processing payment:")
    print(booking)
    # Can do anything here, but aiming to keep it simple (atomic)
    order_id = booking['order_id']
    # If customer id contains "ERROR", simulate failure
    if "ERROR" in booking['']:
        code = 400
        message = 'Simulated failure in shipping record creation.'
    else:  # simulate success
        code = 201
        message = 'Simulated success in shipping record creation.'

    print(message)
    print()  # print a new line feed as a separator

    return {
        'code': code,
        'data': {
            'order_id': order_id

        },
        'message': message
    }


email_sender = 'smoothairlines@gmail.com'
email_password = os.environ.get("EMAIL_PASSWORD")
print(email_password)
# email_password = 'ahmvlesdtbkpquqi'

# get from booking microservice (from passengers.sql)
email_receiver = 'bckf2000@gmail.com' 

subject_payment = "Payment Successful"
body_payment = """
Dear customer,

Thank you for your purchase with SMOOth Airlines. Your payment is successful. This is not a receipt.

We look forward to serving you on your flight with us!

***This message is automatically generated, please do not reply to this email.*** 

- Your friendly SMOOth Crew   

"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())



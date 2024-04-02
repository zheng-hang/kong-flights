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

notif_queue_name = os.environ.get('exchangename') or 'Notif'

notif_queue_name = os.environ.get('exchangename') or 'Notif'

app = Flask(__name__)

CORS(app)

# Set env path
dotenv_path = 'vue-frontend/.env'
# Load environment variables from .env file
load_dotenv(dotenv_path)

# Email details
# Email details
email_sender = 'smoothairlines@gmail.com'
email_password = os.environ.get("EMAIL_PASSWORD")

# Receive notif
def receivePaymentUpdate(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=notif_queue_name, on_message_callback=callback, auto_ack=True)
        print('notifications: Consuming from queue:', notif_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
        
    except pika.exceptions.AMQPError as e:
            print(f"notifications: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("notifications: Program interrupted by user.")

# Run function based on the message
def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nflights: Received an update by " + __file__)
    if __file__ == "makebooking.py": 
        createPaymentEmail(json.loads(body))  
    # elif __file__ == "booking.py":
    elif __file__ == "amqpNotifTest.py":
        # booking confirmation info
        createBookingEmail(json.loads(body))
    elif __file__ == "seatchange.py":
        createSeatChangeEmail(json.loads(body))
    # DELETE IF APPLICABLE
    # else:
    #     createPaymentEmail(json.loads(body))

    print()

def sendEmail(email_receiver,subject,body):
    try:
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        
        print("Email sent successfully!")
        return jsonify({
            "code": 250,
            "message": "Email sent successfully."
        }), 250

    #ERROR HANDLING
    except smtplib.SMTPAuthenticationError:
        print("Error: SMTP authentication failed. Check your email credentials.")
        return jsonify({
            "code": 401,
            "message": "SMTP authentication failed. Check your email credentials."
        }), 401
     
    except smtplib.SMTPException as e:
        print(f"Error: SMTP error occurred. {e}")
        return jsonify({
            "code": 500,
            "message": f"SMTP error occured: {e}"
        }), 500
    
    except Exception as e:
        print(f"Error: An unexpected error occurred. {e}")
        return jsonify({
            "code": 500,
            "message": f"An unexpected error occurred: {e}"
        }), 500

# To send successful Payment Email 
def createPaymentEmail(msg):
    # get from booking microservice (from passengers.sql)
    email_receiver = msg.email 
    
    subject = "Payment Successful"
    body = """
    Dear customer,

    Thank you for your purchase with SMOOth Airlines. Your payment is successful and your booking is processing. You will receive a separate email upon successful booking.
    
    Please note that this is not a receipt.

    We look forward to serving you on your flight with us!

    ***This message is automatically generated, please do not reply to this email.*** 

    - Your friendly SMOOth Crew   

    """
    sendEmail(email_receiver, subject, body)
    

# To send successful Booking Email 
def createBookingEmail(msg):
    # get from booking microservice (from passengers.sql)
    email_receiver = msg.email 
    
    subject = "Booking Successful"
    body = f"""
    Dear customer,

    Thank you for choosing SMOOth Airlines as the carrier for your trip! Your booking has been confirmed with the following details:

    Booking ID: {msg.bid}
    Passenger ID: {msg.pid}
    Flight: {msg.fid}
    Seat: {msg.seatcol}{msg.seatnum}

    We look forward to serving you on your flight with us!

    ***This message is automatically generated, please do not reply to this email.*** 

    - Your friendly SMOOth Crew   

    """
    sendEmail(email_receiver, subject, body)

# To send successful Booking Email 
# NEED TO CHANGE BODY MESSAGE TO INCLUDE/EXCLUDE OLD SEAT
def createSeatChangeEmail(msg):
    # get from booking microservice (from passengers.sql)
    email_receiver = msg.email 
    
    subject = "Flight Seat Change Successful"
    body = f"""
    Dear customer,

    We are pleased to inform you that your seat has been changed. Your flight details are as follows:

    OldSeat-> {msg.seatcol}{msg.seatnum} 

    Once again, thank you for choosing SMOOth Airlines, we look forward to serving you on your flight!

    ***This message is automatically generated, please do not reply to this email.*** 

    - Your friendly SMOOth Crew   

    """

    sendEmail(email_receiver, subject, body)


## LAUNCHING FLASK CONNECTION AND AMQP CHANNEL ##

def start_flask():
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        print("Flask thread exiting")

def start_amqp():
    try:
        print("notifications: Getting Connection")
        connection = amqp_connection.create_connection()  # get the connection to the broker
        print("notifications: Connection established successfully")
        channel = connection.channel()
        receivePaymentUpdate(channel)
    finally:
        print("AMQP thread exiting")

# Start script execution
if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    amqp_thread = threading.Thread(target=start_amqp)

    flask_thread.start()
    amqp_thread.start()
    
    try:
        flask_thread.join()
        amqp_thread.join()

    except KeyboardInterrupt:
        print("Keyboard interrupt received, exiting threads")

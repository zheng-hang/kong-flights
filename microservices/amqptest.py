from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import pika
import json
import amqp_connection

app = Flask(__name__)
CORS(app)

exchangename = environ.get('exchangename') #order_topic
exchangetype = environ.get('exchangetype') #topic 

print("amqptest: Getting Connection")
connection = amqp_connection.create_connection()  # get the connection to the broker
print("amqptest: Connection established successfully")
channel = connection.channel()

## FORMAT FOR BODY - CreateBooking    ##
## Routing Key: #.booking             ##
# {
#     "pid": 1,
#     "fid": "SQ 123",
#     "seatcol": "A",
#     "seatnum": 1
# }

createBooking = {
                    "pid": 1,
                    "fid": "SQ 123",
                    "seatcol": "A",
                    "seatnum": 1
                }

## FORMAT FOR BODY - Update Seat    ##
## Routing Key: #.booking           ##
# {
#     "bid",
#     "seatcol": "A",
#     "seatnum": 1
# }

seatupdate = {
                "bid": 3,
                "seatcol": "A",
                "seatnum": 1
            }

@app.route("/testamqp/bookings")
def amqptest():
    print('\n\n-----Publishing the (seatupdate) message with routing_key=seatupdate.booking-----')

    # Ensuring message structure aligns with what the receiver expects
    message = json.dumps(seatupdate)  # seatupdate already has 'seatnum' as per the receiver's expectation
    
    # Publishing the message to the AMQP exchange with the correct routing key
    channel.basic_publish(exchange=exchangename, routing_key="seatupdate.booking", 
                          body=message, properties=pika.BasicProperties(delivery_mode=2))

    print("\nSeat update request published to the RabbitMQ Exchange:", seatupdate)

    print('\n\n-----Publishing the (bookingcreation) message with routing_key=createbooking.booking-----')

    # Ensuring message structure aligns with what the receiver expects
    message = json.dumps(createBooking)  # seatupdate already has 'seatnum' as per the receiver's expectation
    
    # Publishing the message to the AMQP exchange with the correct routing key
    channel.basic_publish(exchange=exchangename, routing_key="createbooking.booking", 
                          body=message, properties=pika.BasicProperties(delivery_mode=2))

    print("\nBooking creation request published to the RabbitMQ Exchange:", createBooking)

    # Returning a more relevant response
    return jsonify({
        "code": 200,  # Assuming successful publication, setting a success status code
        "data": {"seatupdate": seatupdate, "createBooking": createBooking},
        "message": "Seat update and create booking request successfully published."
    })
    



if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
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

exchangename = environ.get('exchangename') #seat_topic
exchangetype = environ.get('exchangetype') #topic 

print("amqptest: Getting Connection")
connection = amqp_connection.create_connection()  # get the connection to the broker
print("amqptest: Connection established successfully")
channel = connection.channel()
# Create the message


@app.route("/testamqp/bookings")
def amqptest():
    print('\n\n-----Publishing the (seatupdate) message with routing_key=tryseat.seat-----')

    message = {
    'fid': 'LH 520',
    'seatcol': 'A',
    'seatnum': 1,
    'available': 1,
    'price': 25.00,
    'seat_class': 'first'
    }

    # Ensuring message structure aligns with what the receiver expects
    messages = json.dumps(message)  # seatupdate already has 'seatnum' as per the receiver's expectation
    
    # Publishing the message to the AMQP exchange with the correct routing key
    channel.basic_publish(exchange=exchangename, routing_key="try.seat", 
                          body=messages, properties=pika.BasicProperties(delivery_mode=2))

    print("\nBooking creation request published to the RabbitMQ Exchange:", messages)

    # Returning a more relevant response
    return jsonify({
        "code": 200,  # Assuming successful publication, setting a success status code
        "data": {"message": messages},
        "message": "Seat update and create booking request successfully published."
    })
    

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5101, debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

# To call HTTP
import requests
from invokes import invoke_http

# To call AMQP
import pika
import json
import amqp_connection

app = Flask(__name__)
CORS(app)

exchangename = environ.get('exchangename') or 'notif_topic'
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
                    "seatnum": 1,
                    "email": "bckf2000@gmail.com",
                }

## FORMAT FOR BODY - Update Seat    ##
## Routing Key: #.booking           ##
# {
#     "bid",
#     "seatcol": "A",
#     "seatnum": 1
# }

seatupdate = {
                "email": "bckf2000@gmail.com",
                "bid": 3,
                "seatcol": "A",
                "seatnum": 1
            }

@app.route("/testamqp/bookings")
def amqptest_booking():
    print('\n\n-----Publishing the (bookingcreation) message with routing_key=bookingupdate.notif-----')

    # Ensuring message structure aligns with what the receiver expects
    message = json.dumps(createBooking)  # seatupdate already has 'seatnum' as per the receiver's expectation
    
    # Publishing the message to the AMQP exchange with the correct routing key
    channel.basic_publish(exchange=exchangename, routing_key="bookingupdate.notif", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    print("\nBooking creation request published to the RabbitMQ Exchange:", createBooking)

    # Returning a more relevant response
    return jsonify({
        "code": 200,  # Assuming successful publication, setting a success status code
        "data": {"seatupdate": seatupdate, "createBooking": createBooking},
        "message": "Seat update and create booking request successfully published."
    })
    

# CREATE TABLE IF NOT EXISTS flights (
#     FID VARCHAR(6) NOT NULL PRIMARY KEY,
#     Airline VARCHAR(255),
#     DepartureLoc VARCHAR(255),
#     ArrivalLoc VARCHAR(255),
#     Date DATE,
#     DepartureTime TIME,
#     Duration INT,
#     Price DOUBLE
# );

insertFlights = [{  "FID": "LH111",
                    "Airline": "Lufthansa",
                    "DepartureLoc": "Johor Bahru",
                    "ArrivalLoc": "Singapore",
                    "Date": "2024-03-15",
                    "DepartureTime": "10:30:00",
                    "Duration": 60,
                    "Price": 140.50
                },
                {   "FID": "LH112",
                    "Airline": "Lufthansa",
                    "DepartureLoc": "Jakarta",
                    "ArrivalLoc": "Singapore",
                    "Date": "2024-03-15",
                    "DepartureTime": "10:30:00",
                    "Duration": 120,
                    "Price": 280.50
                }]

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
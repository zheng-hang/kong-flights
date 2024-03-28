#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import amqp_connection
import json
import pika
from os import environ


seatchange_queue_name = environ.get('avail_queue_name') or 'SeatUpdate'
new_queue_name = environ.get('new_queue_name') or 'NewBooking'


# Receive seat change
def receiveUpdateLog(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=seatchange_queue_name, on_message_callback=callback_update, auto_ack=True)
        print('bookings: Consuming from queue:', seatchange_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"bookings: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("bookings: Program interrupted by user.")

## FORMAT FOR BODY - Update Seat    ##
## Routing Key: #.seatUpdate             ##
# {
#     "email": "emily.jones987@example.org",
#     "fid": "SQ 123",
#     "seatcol": "A",
#     "seatno": 1
# }

def callback_update(channel, method, properties, body): # required signature for the callback; no return
    print("\nbookings: Received an update by " + __file__)
    processUpdate(json.loads(body))
    print()

def processUpdate(update):
    print("bookings: Recording an update:")
    print(update)




# Receive new booking
def receiveCreationLog(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=new_queue_name, on_message_callback=callback_creation, auto_ack=True)
        print('bookings: Consuming from queue:', new_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"bookings: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("bookings: Program interrupted by user.")


## FORMAT FOR BODY - CreateBooking    ##
## Routing Key: *.newBooking          ##
# {
#     "email": "emily.jones987@example.org",
#     "fid": "SQ 123",
#     "seatcol": "A",
#     "seatno": 1
# }

def callback_creation(channel, method, properties, body): # required signature for the callback; no return
    print("\nbookings: Received an creation by " + __file__)
    processCreation(json.loads(body))
    print()

def processCreation(update):
    print("bookings: Recording a creation:")
    print(update)


# GET passenger bookings












if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("bookings: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("bookings: Connection established successfully")
    channel = connection.channel()
    receiveUpdateLog(channel)
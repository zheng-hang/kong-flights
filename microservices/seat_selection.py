#!/usr/bin/env python3
import amqp_connection
import json
import pika
from os import environ


avail_queue_name = environ.get('avail_queue_name') or 'SeatAvailUpdate'
new_queue_name = environ.get('new_queue_name') or 'NewSeatUpdate'


def receiveUpdateLog(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=avail_queue_name, on_message_callback=callback, auto_ack=True)
        print('seat: Consuming from queue:', avail_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"seat: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("seat: Program interrupted by user.")


## FORMAT FOR BODY - Update seat    ##
## Routing Key: #.avail             ##
# {
#     "FID": "FL123",
#     "SeatCol": "A",
#     "SeatNum: 1,
#     "Available": true
# }

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nseat: Received an update by " + __file__)
    processUpdate(json.loads(body))
    print()

def processUpdate(update):
    print("seat: Recording an update:")
    print(update)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("seat: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("seat: Connection established successfully")
    channel = connection.channel()
    receiveUpdateLog(channel)
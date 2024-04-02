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


seat_URL = environ.get("seat_URL") or "http://localhost:5000/seat"
passengerbooking_URL = environ.get("passengerbooking_URL") or "http://localhost:5000/booking"
# payment_url =
# notification_url = ""



exchangename_booking = "booking_topic"
exchangename_seat_change =  "seat_change_topic"
# exchangename_notification = "" not done
# exchangename_payment = "" not done

exchangetype="topic"

#create a connection and a channel to the broker to publish messages to seat_, passengerbookigns, notifications and 
connection = amqp_connection.create_connection() 
channel = connection.channel()

#if the exchange is not yet created, exit the program ()
if not amqp_connection.check_exchange(channel, exchangename_seat_change, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

if not amqp_connection.check_exchange(channel, exchangename_booking, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status




@app.route("/seatchange", methods=['POST'])
def seat_change():

        data = {
            'bid': 1,
            'fid': 'LH 520',
            'seatcol': 'A',
            'seatnum': 1,
        }

        result = processSeatChange(data)
        print('\n------------------------')
        print('\nresult: ', result)



def processSeatChange(seat):
    # send the seat change into seat
    # invoke seat microservice

    print("invoking seat microservice")

    # scenario 2: reserving the seat
    try:
        channel.basic_publish(exchange=exchangename_seat_change, routing_key="Reserve.seat", 
                            body=seat, properties=pika.BasicProperties(delivery_mode=2)) 
        print("Reserve seat request published to the RabbitMQ Exchange:", seat)  

    except Exception as e:
        print("An error occurred at scenario 1:", e)
        return #exit the function if scenario 1 fails
    
    # UNCOMMENT ONCE PAYMENT IS DONE
    #scenario 3-7: send payment requests to payment system (NOT DONE)
    # try:
    #     price_result = invoke_http(payment_url, method='POST', json=seat)
    #     print("Payment request sent to payment system")
    # except Exception as e:
    #     print("An error occurred:", e)
    #     # this scenario will trigger if any of the above steps have failed but if scenario 2 is successful
    #     #scenario 8: If fail, updating old seat availability
    #     channel.basic_publish(exchange=exchangename_seat_change, routing_key="Update.Failseat",
    #                             body=seat, properties=pika.BasicProperties(delivery_mode=2))


    #scenario 9: send to notification (NOT DONE)

    #scenario 10: update passenger bookings
    # this case is seat change so bid in message 
    channel.basic_publish(exchange=exchangename_booking, routing_key="seatupdate.booking", 
                          body=seat, properties=pika.BasicProperties(delivery_mode=2))

    #scenario 12: Update old flight seat to available
    # first get the fid,seatcol and seatnum of the old seat
    person_pid = seat['pid']
    original_seat = get_original_booking(person_pid)
    channel.basic_publish(exchange=exchangename_seat_change, routing_key="Update.Failseat", 
                            body=original_seat, properties=pika.BasicProperties(delivery_mode=2))
    
    print("\nSeat update request published to the RabbitMQ Exchange:")

    print('\n\n-----Publishing the (bookingcreation) message with routing_key=createbooking.booking-----')

    # UNCOMMENT ONCE EVERYTHING IS DONE
    #scenario 8: returning the output to the UI
    # return {
    #     "payment_details" : price_result,
    #     "seat" : seat,
    # }

# for retrieving the person's original bid
def get_original_booking(person_pid):
    response = requests.get(f"http://localhost:5000/booking/{person_pid}")
    data = response.json()
    if data['code'] == 200 and data['data']:
        return data['data'][0]
    return None
 



if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5105, debug=True)
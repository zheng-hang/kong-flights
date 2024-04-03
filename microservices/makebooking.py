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


flight_URL = environ.get('flight_URL') or "http://flight:5000/flight/price/" 
seatReserve_URL = environ.get("seatReserve_URL") or "http://localhost:5000/reserveseat"
newBooking_URL = environ.get("newBooking_URL") or "http://bookings:5000/newbooking"
# payment_URL = environ.get('payment_URL')


# seat_exchangename = environ.get('seat_exchangename') or "seat_topic" # seat exchange name
# booking_exchangename = environ.get('booking_exchangename') or "booking_topic" #booking exchange name
# notif_exchangename = environ.get('notif_exchangename') or 'notif_topic'
# exchangetype="topic" # use a 'topic' exchange to enable interaction

# Instead of hardcoding the values, we can also get them from the environ as shown below
# exchangename = environ.get('exchangename') #order_topic
# exchangetype = environ.get('exchangetype') #topic 

#create a connection and a channel to the broker to publish messages to activity_log, error queues
# connection = amqp_connection.create_connection() 
# channel = connection.channel()

# #if the seat exchange is not yet created, exit the program
# if not amqp_connection.check_exchange(channel, seat_exchangename, exchangetype):
#     print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
#     sys.exit(0)  # Exit with a success status

# #if the booking exchange is not yet created, exit the program
# if not amqp_connection.check_exchange(channel, booking_exchangename, exchangetype):
#     print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
#     sys.exit(0)  # Exit with a success status


# JSON RESPONSE FORMAT
# {
#     'email': 'help@gmail.com',
#     'fid': 'SQ 123',
#     'seatcol': 'A',
#     'seatnum': 1
# }

@app.route("/make_booking", methods=['POST'])
def place_order():
    # Simple check of input format and data of the request are JSON
    #SCENARIO 1: Receive booking request
    if request.is_json:
        try:
            booking = request.get_json()
            print("\nReceived a booking request in JSON:", booking)

            # do the actual work
            # 1. Send booking info
            result = processBookingRequest(booking)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "makebooking.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processBookingRequest(booking):
    # 2-3. Get flight price
    # Invoke the flight microservice
    print('\n-----Invoking flight microservice-----')
    price = invoke_http((flight_URL + booking.FID), method='GET')
    print('flight price:', price['data'])

    if price['code'] == 404:
        print('\n-----'+ price['message'] +'-----')
        return {
            "code": 500,
            "data": {"priceRetrieval_result": price},
            "message": "Price not found."
        }


    # 4-5. reserve seat in Seats
    message = {
                    'fid': booking['fid'],
                    'seatcol': booking['seatcol'],
                    'seatnum': booking['seatnum']
                }

    # print('\n\n-----Publishing the (seatupdate) message with routing_key=booking.seat-----')

    # channel.basic_publish(exchange=seat_exchangename, routing_key="booking.seat", 
    #     body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    # print("\nSeat update request published to the RabbitMQ Exchange:", message)
    print("invote_http for reserve_seat")
    reserve_seat = invoke_http(seatReserve_URL, method='PUT', json=message)
    code_reserve_seat = reserve_seat['code']
    if code_reserve_seat not in range(200, 300):
        return {
            "code": 500,
            "data": "Seat reservation failed"
        }
    
    # 6-9. Call payment svc
    # print('\n-----Call payment service-----')
    # payment_result = invoke_http(payment_URL, method='POST', json=price)
    # print('payment_result:', payment_result)
    # if payment_result["code"] in range (200,300):
    #     return {
    #         "code": 500,
    #         "data": {
    #             "payment_result": payment_result,
    #         },
    #         "message": "Payment failed."
    #     }

    # 10. Send Notif AMQP
    email = {
                    'email': booking['email'],
                }

    # print('\n\n-----Publishing the (notif) message with routing_key=paymentupdate.notif-----')

    # channel.basic_publish(exchange=notif_exchangename, routing_key="paymentupdate.notif", 
    #     body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    # print("\nNotif request published to the RabbitMQ Exchange:", message)


    # 11. Send booking creation req
    # print('\n\n-----Publishing the (booking creation) message with routing_key=paymentupdate.notif-----')

    # channel.basic_publish(exchange=notif_exchangename, routing_key="paymentupdate.notif", 
    #     body=booking, properties=pika.BasicProperties(delivery_mode = 2)) 

    # print("\nBooking creation request published to the RabbitMQ Exchange:", booking)

    combined = {
        'email': booking['email'],
        'fid': booking['fid'],
        'seatcol': booking['seatcol'],
        'seatnum': booking['seatnum']
    }

    print('\n-----Invoking bookings microservice-----')
    new_booking = invoke_http(newBooking_URL, method='POST', json=combined)
    print('new_booking:', new_booking)

    if new_booking['code'] not in range(200, 300):
        return {
            "code": 500,
            "data": {
                "new_booking": new_booking,
            },
            "message": "Booking failed."
        }

    return {
        "code": 200,
        "data": {
            "price": price,
            "reserve_seat": reserve_seat,
            # "payment_result": payment_result,
            "email": email,
            "new_booking": new_booking
        },
        "message": "Check email for flight details."
    }



# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
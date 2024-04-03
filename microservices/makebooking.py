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
payment_URL = environ.get('payment_URL') or "http://payment:5000/"

seat_exchangename = environ.get('seat_exchangename') or "seat_topic" # seat exchange name
booking_exchangename = environ.get('booking_exchangename') or "booking_topic" #booking exchange name
notif_exchangename = environ.get('notif_exchangename') or 'notif_topic'
exchangetype="topic" # use a 'topic' exchange to enable interaction

email_to_booking = {}
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
    # 2. Get flight price
    # Invoke the flight microservice
    print('\n-----Invoking flight microservice-----')
    price = invoke_http((flight_URL + booking.FID), method='GET')
    print('flight price:', price)

    if price['code'] == 404:
        print('\n-----'+ price['message'] +'-----')
        return {
            "code": 500,
            "data": {"priceRetrieval_result": price},
            "message": "Price not found."
        }


    # 3. reserve seat in Seats
    message = {
                    'fid': booking['fid'],
                    'seatcol': booking['seatcol'],
                    'seatnum': booking['seatnum']
                }

    print('\n\n-----Publishing the (seatupdate) message with routing_key=booking.seat-----')

    channel.basic_publish(exchange=seat_exchangename, routing_key="booking.seat", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    print("\nSeat update request published to the RabbitMQ Exchange:", message)


    # 4. Call payment svc
    print('\n-----Call payment service-----')
    checkout_url = payment_URL + "/endpoint"
    obj = {"email": booking["email"], "price": price["price"]}
    payment_result = invoke_http(checkout_url, method='POST', json=str(obj))
    print('payment_result:', payment_result)

    email_to_booking[booking['email']] = booking
    return {
            "code": 400,
            "data": {
                "payment_result": payment_result,
            },
            "message": "Simulated shipping record error sent for error handling."
        }

@app.route("/webhook", methods=['POST'])
def handle_webhook():
    if not request.is_json:
        return {
            "code": 400,
            "message": "Invalid JSON"
        }
    
    headers = dict(request.headers)
    body = request.get_data(as_text=True)

    response = invoke_http((payment_URL + "/webhook"), method='POST', json=body, headers=headers)
    if response['code'] != 200:
        return {
            "code": 400,
            "message": "Error in payment service"
        }
    
    if "email" not in response:
        return {
            "code": 400,
            "message": "No email in response"
        }

    email = response["email"]
    return jsonify(email=email)


    # message = {
    #     'email': email,
    # }

    # print('\n\n-----Publishing the (notif) message with routing_key=paymentupdate.notif-----')

    # channel.basic_publish(exchange=notif_exchangename, routing_key="paymentupdate.notif", 
    #     body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    # print("\nNotif request published to the RabbitMQ Exchange:", message)


    # # 6. Send booking creation req
    # print('\n\n-----Publishing the (booking creation) message with routing_key=paymentupdate.notif-----')

    # channel.basic_publish(exchange=notif_exchangename, routing_key="paymentupdate.notif", 
    #     body=email_to_booking[email], properties=pika.BasicProperties(delivery_mode = 2)) 

    # print("\nBooking creation request published to the RabbitMQ Exchange:", email_to_booking[email])

    # del email_to_booking[email]

    # return jsonify({
    #             'code': 200,
    #             'message': "Payment successful, booking creation sent"
    #         })

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
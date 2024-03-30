import pika
import json
import amqp_connection


# Establish a connection to RabbitMQ
print("amqptest: Getting Connection")
connection = amqp_connection.create_connection()  # get the connection to the broker
print("amqptest: Connection established successfully")
channel = connection.channel()
# Declare the queue where the message will be sent
channel.queue_declare(queue='SeatUpdate', durable=True)

# Create the message
message = {
    'fid': 'SQ 123',
    'seatcol': 'B',
    'seatnum': 1,
    'available': 1,
    'price': 30.00,
    'seat_class': 'first'
}
message_json = json.dumps(message)

# Send the message to the queue
channel.basic_publish(exchange='seat_topic', routing_key='update.seat', body=message_json)

# Close the connection
connection.close()
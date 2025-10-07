import jwt
import pika
import os
import json
import config 

def publish_message(event_type, user_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBITMQ))
    channel = connection.channel()
    channel.queue_declare(queue='users_queue')

    event = {
        'event': event_type,
        'user_id': user_id
    }
    
    channel.basic_publish(exchange='', routing_key='users_queue', body=json.dumps(event))
    connection.close()

# Check if password is valid
def is_valid_password(password):
    if len(password) < 8:
        return False
    return True


import jwt
import pika
import os
import json
import config 

def publish_message(event_type, user_id):
    credentials = pika.PlainCredentials(config.RABBITMQ_USER, config.RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBITMQ, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='users_queue', durable=True)

    event = {
        'event': event_type,
        'user_id': user_id
    }
    
    channel.basic_publish(exchange='', routing_key='users_queue', body=json.dumps(event), properties=pika.BasicProperties(delivery_mode=2))
    print("DEBUG message sent")
    connection.close()

# Check if password is valid
def is_valid_password(password):
    if len(password) < 8:
        return False
    return True


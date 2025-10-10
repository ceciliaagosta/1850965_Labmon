from pika.exceptions import AMQPConnectionError
import time
import pika
import config 
import json

# Retry connection function for RabbitMQ
def retry_connection(connect_fn, retries=5, delay=3, backoff=2):
    """
    Retry connecting to RabbitMQ or any service.
    
    :param connect_fn: Function that returns a connection (e.g., pika.BlockingConnection)
    :param retries: Number of retries before giving up
    :param delay: Initial delay in seconds
    :param backoff: Multiplier for exponential backoff
    :return: Connected object
    :raises: Last exception if connection fails after all retries
    """
    attempt = 0
    current_delay = delay
    while attempt < retries:
        try:
            return connect_fn()
        except AMQPConnectionError as e:
            attempt += 1
            if attempt == retries:
                raise
            print(f"Connection failed (attempt {attempt}/{retries}): {e}. Retrying in {current_delay}s...")
            time.sleep(current_delay)
            current_delay *= backoff

# Publish message to RabbitMQ
def publish_message(event_type, monster_id, catch_rate, rarity, collection):
    def connect():
        credentials = pika.PlainCredentials(config.RABBITMQ_USER, config.RABBITMQ_PASS)
        return pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBITMQ_HOST, credentials=credentials))
    connection = retry_connection(connect, retries=5)

    channel = connection.channel()
    channel.queue_declare(queue='monsters_queue', durable=True)

    event = {
        'event': event_type,
        'monster_id': monster_id,
        'catch_rate': catch_rate,
        'rarity': rarity,
        'collection': collection
    }

    channel.basic_publish(exchange='', routing_key='monsters_queue', body=json.dumps(event), properties=pika.BasicProperties(delivery_mode=2))
    print("DEBUG message sent")
    connection.close()
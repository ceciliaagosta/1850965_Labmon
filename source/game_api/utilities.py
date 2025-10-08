# Utility functions
from datetime import datetime, timezone
import config
import random
from models import db, Player, MonsterStats, ItemStats
import time
import json
import pika
from pika.exceptions import AMQPConnectionError

# Rarity weight function - returns a weights for rarity levels 1 to 5 based on time passed since last encounter
def rarity_weights(last_encounter_time):
    if last_encounter_time is None:
        return [1, 0, 0, 0, 0]  # if first encounter ever, only rarity 1
    
    time_diff = (datetime.now(timezone.utc) - last_encounter_time).total_seconds() / 60  # in minutes

    if time_diff < 30:
        return []
    
    # Define base weights for rarities 1 to 5
    base = config.BASE_WEIGHTS.copy()

    # Increase weights for higher rarities based on time passed
    # Every half hour passed increases chance of rare monsters slightly
    factor = min(time_diff / 30, 3)  # cap effect at 3 hours

    # Shift weight toward rare monsters
    adjusted = [
        max(1, base[0] - factor * 5),
        max(1, base[1] - factor * 2),
        base[2] + factor * 2,
        base[3] + factor * 3,
        base[4] + factor * 4
    ]

    # Normalize
    total = sum(adjusted)
    return [w / total for w in adjusted]

# Rarity selection function
def choose_rarity(weights):
    if weights == []:
        return 0  # if weights list is empty, return rarity 0 (no encounter)
    return random.choices(config.RARITY_LEVELS, weights=weights, k=1)[0]

# Monster selection function
def select_monster(encounter_pool):
    return random.choice(encounter_pool)[0]  # return the first element which is the monster_id

# Catch attempt function
def attempt_catch(catch_rate, item_effect):
    adjusted_rate = catch_rate * item_effect
    return random.random() < adjusted_rate

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

# Start RabbitMQ consumer with retries
def start_consumer(app, queue_name, callback, host, retries=5):
    def connect():
        credentials = pika.PlainCredentials(config.RABBITMQ_USER, config.RABBITMQ_PASS)
        return pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))
    
    connection = retry_connection(connect, retries=retries)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    print(f"Consumer connected to queue '{queue_name}'")
    
    callback = generic_callback(queue_name, app)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# General callback for RabbitMQ consumer
def generic_callback(queue_name, app):
    """
    Returns a pika callback function that handles messages
    based on the queue_name.
    """
    def callback(ch, method, properties, body):
        with app.app_context():
            try:
                message = json.loads(body)
                if queue_name == "users_queue":
                    player_event_handler(message)
                    # add other queues here:
                    # elif queue_name == "items_queue":
                    #     items_queue_handler(message)
                else:
                    print(f"No handler defined for queue '{queue_name}'")
            except Exception as e:
                print(f"Error processing message from queue '{queue_name}': {e}")       
    return callback

# Event handler for user events for RabbitMQ consumer
def player_event_handler(message):
    try:
        event_type = message.get("event")
        user_id = message.get("user_id")
        if event_type == 'user_deleted':
            # Delete associated player data
            player = Player.query.filter_by(player_id=user_id).first()
            if player:
                db.session.delete(player)
                db.session.commit()
                print(f"Deleted player data for player_id {user_id}")
        elif event_type == 'user_created':
            # Create associated player data if not exists
            if not Player.query.filter_by(player_id=user_id).first():
                new_player = Player(player_id=user_id)
                db.session.add(new_player)
                db.session.commit()
                print(f"Created player data for player_id {user_id}")
    except Exception as e:
        print(f"Error handling event: {e}")
        pass

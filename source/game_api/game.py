from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Encounter, Player, Collection, Inventory, MonsterStats, ItemStats
import jwt
import config
import utilities
from functools import wraps
import time
from datetime import datetime, timezone
import sqlalchemy.exc
import pika
import os
import json
import threading

app = Flask(__name__)
app.config.from_object(config)
CORS(app) # TODO: All origins allowed; dev only?
db.init_app(app)

# Create tables on first run
with app.app_context():
    retries = 5
    while retries > 0:
        try:
            db.create_all()
            break
        except sqlalchemy.exc.OperationalError:
            retries -= 1
            print("Database not ready, retrying in 5s...")
            time.sleep(5)
    else:
        raise Exception("Database connection failed after retries")
    
def consume_player_events():
    try: 
        credentials = pika.PlainCredentials(config.RABBITMQ_USER, config.RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBITMQ, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='users_queue', durable=True)

        def callback(ch, method, properties, body):
            message = json.loads(body)
            utilities.player_event_handler(message)

        channel.basic_consume(queue='users_queue', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error : Could not connect to RabbitMQ: {e}")

# Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            token = auth_header.split(" ")[1]  # "Bearer <token>"
            data = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])   
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(data, *args, **kwargs)
    return decorated

# Admin required decorator
def admin_required(f):
    @token_required  # ensures the user is logged in
    @wraps(f)
    def decorated(data, *args, **kwargs):
        if data['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(data, *args, **kwargs)
    return decorated

# Routes

# Get all encounters (admin only)
@app.route('/game/encounters', methods=['GET'])
@admin_required
def get_all_encounters(data):
    encounters = Encounter.query.all()
    return jsonify([e.to_dict() for e in encounters]), 200

# Generate a new encounter
@app.route('/game/encounters', methods=['POST'])
@token_required
def generate_encounter(data):
    # Get player info and last encounter time
    user_id = data.get('user_id')
    player = Player.query.filter_by(player_id=user_id).first()
    last_encounter = player.lastEncounter_id
    last_encounter_time = Encounter.query.filter_by(id=last_encounter).first().timestamp if last_encounter else None

    # Determine rarity based on time since last encounter
    weights = utilities.rarity_weights(last_encounter_time)
    rarity = utilities.choose_rarity(weights)
    if rarity == 0:
        return jsonify({'message': 'No encounter this time'}), 403

    # Select a monster from the database based on rarity
    encounter_pool = MonsterStats.query.filter_by(rarity=rarity).all()
    if not encounter_pool:
        return jsonify({'error': 'No monsters available for this rarity'}), 500
    selected_monster = utilities.select_monster(encounter_pool)

    # Create and store the encounter
    encounter = Encounter(player_id=player, monster_id=selected_monster, isCaught=False)
    player.lastEncounter_id = encounter.id
    db.session.add(encounter)
    db.session.commit()

    return jsonify({'message': 'Encounter generated', 'encounter_id': encounter.id, 'monster_id': selected_monster}), 200

# Get a specific encounter's details
@app.route('/game/encounters/<int:encounter_id>', methods=['GET'])
@token_required
def get_encounter(data, encounter_id):
    encounter = Encounter.query.filter_by(id=encounter_id).first()
    if not encounter:
        return jsonify({'error': 'Encounter not found'}), 404
    return jsonify(encounter.to_dict()), 200

# Run away from an encounter
@app.route('/game/encounters/<int:encounter_id>', methods=['DELETE'])
@token_required
def delete_encounter(data, encounter_id):
    encounter = Encounter.query.filter_by(id=encounter_id).first()
    if not encounter:
        return jsonify({'error': 'Encounter not found'}), 404
    db.session.delete(encounter)
    db.session.commit()
    return jsonify({'message': 'Encounter deleted'}), 200

# Catch a monster in an encounter
@app.route('/game/encounters/<int:encounter_id>/catch', methods=['POST'])
@token_required
def catch_monster(data, encounter_id):
    body = request.get_json() or {}
    item_id = body.get('item_id')

    player = Player.query.filter_by(player_id=data.get('user_id')).first()
    if not player:
        return jsonify({'error': 'Player not found'}), 404

    # Validate encounter and player ownership
    encounter = Encounter.query.filter_by(id=encounter_id).first()
    if not encounter:
        return jsonify({'error': 'Encounter not found'}), 404
    if encounter.player_id != player.player_id:
        return jsonify({'error': 'Unauthorized action'}), 403
    if encounter.isCaught:
        return jsonify({'error': 'Monster already caught'}), 400
    
    # Check if the monster exists
    monster = MonsterStats.query.filter_by(id=encounter.monster_id).first()
    if not monster:
        return jsonify({'error': 'Monster data not found'}), 500
    catch_rate = monster.catch_rate
    rarity = monster.rarity

    # Check if the item exists
    if item_id is None:
        item = None  # No item used
        item_effect = 1  # Default effect
    else:
        item = ItemStats.query.filter_by(id=item_id).first()
        if not item:
            return jsonify({'error': 'Item data not found'}), 500
        
        inventory_entry = Inventory.query.filter_by(player_id=player.player_id, item_id=item.item_id).first()
        if not inventory_entry or inventory_entry.qty <= 0:
            return jsonify({'error': 'Item not in inventory'}), 400
        
        item_effect = item.effect

    # Attempt to catch the monster
    if utilities.attempt_catch(catch_rate, item_effect):
        # Decrease item quantity if used   
        if item:
            inventory_entry.qty -= 1
            if inventory_entry.qty <= 0:
                db.session.delete(inventory_entry)

        encounter.isCaught = True
        # Update player's collection
        collection_entry = Collection.query.filter_by(player_id=encounter.player_id, monster_id=encounter.monster_id).first()
        if not collection_entry:
            collection_entry = Collection(player_id=encounter.player_id, monster_id=encounter.monster_id, qty=1)
            db.session.add(collection_entry)
        else:
            collection_entry.qty += 1

        # Update player's currency based on rarity
        reward = config.REWARDS[rarity - 1]  # rarity is 1-indexed
        player.currency += reward
        db.session.commit()
        return jsonify({'message': 'Monster caught successfully!', 'reward': reward, 'player_currency': player.currency}), 200
    
    else:
        return jsonify({'message': 'Failed to catch the monster.', 'player_currency': player.currency}), 200
    

if __name__ == '__main__':
    threading.Thread(target=consume_player_events, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True) # TODO: Remove debug=True in production
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
    start_timer = player.timer_start if last_encounter else None

    if user_id == 1:
        # Test user: use test rarity weights
        weights = utilities.rarity_weights(start_timer, delay=1)
        rarity = utilities.choose_rarity(weights)
        if rarity == 0:
            return jsonify({'message': '[TEST] No encounter this time'}), 403
    else:
        # Determine rarity based on time since last encounter
        weights = utilities.rarity_weights(start_timer)
        rarity = utilities.choose_rarity(weights)
        if rarity == 0:
            return jsonify({'message': 'No encounter this time'}), 403

    # Select a monster from the database based on rarity
    encounter_pool = MonsterStats.query.filter_by(rarity=rarity).all()
    if not encounter_pool:
        return jsonify({'error': 'No monsters available for this rarity'}), 500
    selected_monster = utilities.select_monster(encounter_pool).monster_id

    # Create and store the encounter
    encounter = Encounter(player_id=player.player_id, monster_id=selected_monster, isCaught=False)
    db.session.add(encounter)
    db.session.flush()  # Get encounter ID before commit
    player.lastEncounter_id = encounter.id
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
    if request.is_json:
        body = request.get_json()
    else:
        body = {}
        
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
    monster = MonsterStats.query.filter_by(monster_id=encounter.monster_id).first()
    if not monster:
        return jsonify({'error': 'Monster data not found'}), 500
    catch_rate = monster.catch_rate
    rarity = monster.rarity

    # Check if the item exists
    if item_id is None:
        item = None  # No item used
        item_effect = 1  # Default effect
    else:
        item = ItemStats.query.filter_by(item_id=item_id).first()
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
    
# Signal start of timer for encounter generation
@app.route('/game/timer', methods=['POST'])
@token_required
def start_timer(data):
    player = Player.query.filter_by(player_id=data.get('user_id')).first()
    if not player:
        return jsonify({'error': 'Player not found'}), 404
    player.timer_start = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({'message': 'Timer started', 'start_time': player.timer_start}), 200

# Get a player's collection
@app.route('/game/collection', methods=['GET'])
@token_required
def get_collection(data):
    player = Player.query.get_or_404(data.get('user_id'))
    collection = Collection.query.with_entities(Collection.monster_id, Collection.qty).filter_by(player_id=player.player_id).all()
    return jsonify({'collection': {monster_id: qty for monster_id, qty in collection}}), 200

# Shard a monster from the player's collection
@app.route('/game/collection/<int:monster_id>/shard', methods=['PUT'])
@token_required
def shard_monster(data, monster_id):
    player = Player.query.get_or_404(data.get('user_id'))
    collection_entry = Collection.query.filter_by(player_id=player.player_id, monster_id=monster_id).first()
    if not collection_entry:
        return jsonify({'error': 'Monster not found in collection'}), 404
    if collection_entry.qty <= 0:
        return jsonify({'error': 'Not enough quantity to shard this monster'}), 400
    
    monster_stats = MonsterStats.query.get_or_404(monster_id)
    rarity = monster_stats.rarity

    try:
        reward = config.SHARD_REWARDS[rarity - 1]
    except IndexError:
        return jsonify({'error': 'Invalid rarity value'}), 400 

    collection_entry.qty -= 1
    player.currency += reward
    db.session.commit()

    return jsonify({'monster_id': monster_id,'new_quantity': collection_entry.qty,'reward': reward,'new_currency': player.currency}), 200

@app.route('/game/collection/claim', methods=['POST'])
@token_required
def claim_collection_rewards(data):
    player= Player.query.get_or_404(data.get('user_id'))
    requested_collection = request.get_json().get('collection')
    if not requested_collection:
        return jsonify({'error': 'No collection data provided'}), 400
    if requested_collection in player.collections_completed:
        return jsonify({'error': 'Collection already claimed'}), 400
    collection_monsters = MonsterStats.query.filter_by(collection=requested_collection).all()
    if not collection_monsters:
        return jsonify({'error': 'Invalid collection specified'}), 400
    counted_monsters = len(collection_monsters)
    owned_monsters = ( db.session.query(Collection).join( MonsterStats, Collection.monster_id == MonsterStats.monster_id )
        .filter( Collection.player_id == player.player_id, MonsterStats.collection == requested_collection, Collection.qty > 0 )
        .count() )
    if counted_monsters != owned_monsters:
        return jsonify({'error': 'Collection not complete'}), 400
    
    reward = config.CLAIM_REWARD 
    player.currency += reward
    current_list = player.collections_completed or []
    current_list.append(requested_collection)
    player.collections_completed = current_list
    db.session.commit()
    return jsonify({'message': 'Collection claimed successfully', 'reward': reward, 'new_currency': player.currency}), 200
    




if __name__ == '__main__':
    threading.Thread(
    target=lambda: utilities.start_consumer(app, "users_queue", utilities.generic_callback("users_queue", app), config.RABBITMQ_HOST, retries=5), daemon=True).start()
    threading.Thread(
        target=lambda: utilities.start_consumer(app, "monsters_queue", utilities.generic_callback("monsters_queue", app), config.RABBITMQ_HOST, retries=5), daemon=True).start()
    threading.Thread(
        target=lambda: utilities.start_consumer(app, "items_queue", utilities.generic_callback("items_queue", app), config.RABBITMQ_HOST, retries=5), daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False) # TODO: Remove debug=True in production
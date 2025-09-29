from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Monster
import jwt
import config
from functools import wraps
import time
import sqlalchemy.exc

ALLOWED_FIELDS = {'name', 'rarity', 'catch_rate', 'collection', 'sprite'}

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
# Get all monsters
@app.route('/monsters', methods=['GET'])
@token_required
def get_monsters(data):
    monsters = Monster.query.all()
    return jsonify([monster.to_dict() for monster in monsters]), 200

# Add a new monster (admin only)
@app.route('/monsters', methods=['POST'])
@admin_required
def add_monster(data):
    monster_data = request.get_json()
    if not monster_data:
        return jsonify({'error': 'No input data provided'}), 400
    
    for field in ALLOWED_FIELDS:
        if field not in monster_data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    if Monster.query.filter_by(name=monster_data['name']).first():
        return jsonify({'error': 'Monster with this name already exists'}), 400
    
    new_monster = Monster(
        name=monster_data['name'],
        rarity=monster_data['rarity'],
        catch_rate=monster_data['catch_rate'],
        collection=monster_data['collection'],
        sprite=monster_data['sprite']
    )
    
    db.session.add(new_monster)
    db.session.commit()
    
    return jsonify(new_monster.to_dict()), 200

# Get, update, or delete a specific monster by ID
@app.route('/monsters/<int:monster_id>', methods=['GET'])
@token_required
def get_monster(data, monster_id):
    monster = Monster.query.get_or_404(monster_id)
    return jsonify(monster.to_dict()), 200

@app.route('/monsters/<int:monster_id>', methods=['PUT'])
@admin_required
def update_monster(data, monster_id):
    monster = Monster.query.get_or_404(monster_id)
    update_data = request.get_json()
    
    if not update_data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Reject invalid keys
    invalid_keys = set(update_data.keys()) - ALLOWED_FIELDS
    if invalid_keys:
        return jsonify({'error': f'Invalid fields: {list(invalid_keys)}'}), 400 
    
    for key in update_data:
        if key == 'name' and Monster.query.filter(Monster.name == update_data['name'], Monster.id != monster.id).first():
            return jsonify({'error': 'Monster with this name already exists'}), 400
        setattr(monster, key, update_data[key])
    
    db.session.commit()
    return jsonify(monster.to_dict()), 200

@app.route('/monsters/<int:monster_id>', methods=['DELETE'])
@admin_required
def delete_monster(data, monster_id):
    monster = Monster.query.get_or_404(monster_id)
    db.session.delete(monster)
    db.session.commit()
    return jsonify({'message': 'Monster deleted'}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True) # TODO: Remove debug=True in production
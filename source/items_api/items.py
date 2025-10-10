from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Item
import config
import jwt
from functools import wraps
import time
import sqlalchemy.exc
import utilities

ALLOWED_FIELDS={'name','price','description', 'effect', 'sprite'}

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
            return jsonify({'message': 'Token is expired!'}), 401

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

#POST PUT DELETE  admin only

# Routes
# Get all items 
@app.route('/items', methods=['GET'])
@token_required
def get_items(data):
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200

# Add a new user (admin only)
@app.route('/items', methods=['POST'])
@admin_required
def add_item(data):
    item_data = request.get_json()
    required_fields=['name','price','description','effect','sprite']
    for field in required_fields:
        if field not in item_data:
            return jsonify({'error': f'Missing field:{field}'}), 400
    if Item.query.filter_by(name=item_data['name']).first():
        return jsonify({'error': 'Item with this name already exists'}), 400
    
    new_item = Item(
        name=item_data['name'],
        price=item_data['price'],
        description=item_data['description'],
        effect=item_data['effect'],
        sprite=item_data['sprite']
    )
    
    db.session.add(new_item)   
    db.session.commit() 
    utilities.publish_message('item_created', new_item.id, new_item.price, new_item.effect)
    return jsonify(new_item.to_dict()), 200

# Get, update, delete user by ID (self or admin)
@app.route('/items/<int:items_id>', methods=['GET'])
@token_required
def get_item(data, item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())

@app.route('/items/<int:item_id>', methods=['PUT'])
@admin_required
def update_item(data, item_id):
    item = Item.query.get_or_404(item_id)
    update_data= request.get_json()

    if not update_data:
        return jsonify({'error': 'No input data provided'}), 400
    
    #Reject invalid keys
    invalid_keys= set(update_data.keys()) - ALLOWED_FIELDS
    if invalid_keys:
        return jsonify({'error': f'Invalid fields:{list(invalid_keys)}'}), 400
    
    for key in update_data:
        if key == 'name' and Item.query.filter(Item.name == update_data['name'], Item.id != item.id).first():
            return jsonify({'error': 'Item with this name already exists'}), 400
        setattr(item, key, update_data[key])

    db.session.commit()
    utilities.publish_message('item_updated', item_id, item.price, item.effect)
    return jsonify(item.to_dict()), 200



@app.route('/items/<int:item_id>', methods=['DELETE'])
@admin_required
def delet_item(data, item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    utilities.publish_message('item_deleted', item_id, item.price, item.effect)
    return jsonify({'message': 'Item deleted'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True) # TODO: Remove debug=True in production

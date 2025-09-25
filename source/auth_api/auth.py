from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, User
import config
import jwt
import datetime
from functools import wraps
import time
import sqlalchemy.exc

VALID_FIELDS = {"username", "email", "role", "password", "old_password"}  # allowed keys to update

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
            # Check if an admin user already exists
            if not User.query.filter_by(role="admin").first():
                admin = User(username="admin", email="admin@example.com", role="admin")
                admin.set_password("password") 
                db.session.add(admin)
                db.session.commit()
                print("Default admin user created: admin / password")
            break
        except sqlalchemy.exc.OperationalError:
            retries -= 1
            print("Database not ready, retrying in 5s...")
            time.sleep(5)
    else:
        raise Exception("Database connection failed after retries")

# Check if password is valid
def is_valid_password(password):
    if len(password) < 8:
        return False
    return True

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
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# Admin required decorator
def admin_required(f):
    @token_required  # ensures the user is logged in
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# Token generation
def generate_token(user_id, secret_key=config.SECRET_KEY, expires_in=config.TTL_ACCESS_TOKEN):
    payload = {
        'user_id': user_id,
        'role': User.query.get(user_id).role,
        'exp': datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

# Token verification
def decode_token(token, secret_key=config.SECRET_KEY):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Routes
# Get all users (admin only)
@app.route('/users', methods=['GET'])
@admin_required
def get_users(current_user):
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Add a new user (admin only)
@app.route('/users', methods=['POST'])
@admin_required
def add_user(current_user):
    data = request.get_json()
    if not data or not 'username' in data or not 'email' in data or not 'password' in data:
        return jsonify({'error': 'Invalid input'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    if 'role' in data:
        role = data['role']
    else:
        role = 'user'
        
    new_user = User(username=data['username'], email=data['email'], role=role)
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 200

# Get, update, delete user by ID (self or admin)
@app.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    if (not current_user or current_user.id != user_id) and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    if (not current_user or current_user.id != user_id) and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    # Reject invalid keys
    invalid_keys = set(data.keys()) - VALID_FIELDS
    if invalid_keys:
        return jsonify({'error': f'Invalid fields: {list(invalid_keys)}'}), 400 
    
    # Reject empty input
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    
    # Update username and email
    if 'username' in data and User.query.filter(User.username == data['username'], User.id != user.id).first():
        return jsonify({'error': 'Username already exists'}), 400
    if 'email' in data and User.query.filter(User.email == data['email'], User.id != user.id).first():
        return jsonify({'error': 'Email already registered'}), 400
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)

    # Update role (admin only)
    if 'role' in data:
        if current_user.role != 'admin':
            return jsonify({'error': 'Only admins can change roles'}), 403
        else:
            user.role = data['role']

    # Update password (self only)
    if 'password' in data:
        if current_user.id != user_id:
           return jsonify({'error': 'Password can only be changed by the user themselves'}), 403
        elif 'old_password' in data and user.check_password(data['old_password']):
            if is_valid_password(data['password']):
                user.set_password(data['password'])
            else:
                return jsonify({'error': 'Invalid password format'}), 400
        else:
            return jsonify({'error': 'Old password is missing or incorrect'}), 400

    db.session.commit()
    return jsonify(user.to_dict()), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    if (not current_user or current_user.id != user_id) and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

# User registration and login
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not 'username' in data or not 'email' in data or not 'password' in data:
        return jsonify({'error': 'Invalid input'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    token = generate_token(new_user.id)
    return jsonify({'token': token}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not 'username' in data or not 'password' in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = generate_token(user.id)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True) # TODO: Remove debug=True in production
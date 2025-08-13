from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task

auth_routes = Blueprint('auth', __name__)


# ======== AUTH ROUTES ========
@auth_routes.route('/auth', methods=['GET'])
def server():
    return({"message": " auth router"})

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful"},session)
    return jsonify({"error": "Invalid credentials"}), 401

@auth_routes.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out"})

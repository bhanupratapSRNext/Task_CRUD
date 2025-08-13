from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task

auth_routes = Blueprint('auth', __name__)


# ======== AUTH ROUTES ========
@auth_routes.route('/auth', methods=['GET'])
def server():
    return({"message": " auth router"})

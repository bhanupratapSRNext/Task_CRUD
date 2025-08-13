from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task

task_routes = Blueprint('tasks', __name__)

# ======== AUTH ROUTES ========
@task_routes.route('/task', methods=['GET'])
def server():
    return({"message": " task router"})

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import re
from email.utils import parseaddr
from flask import render_template,redirect, url_for


auth_routes = Blueprint("auth", __name__)

# EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")


@auth_routes.route("/home")
def home_page():
    return render_template("home.html")


@auth_routes.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("signup.html")
    # data = request.json
    data = {
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }
    email = data.get("email")
    password = data.get("password")

    # Basic validation
    if not email or '@' not in parseaddr(email)[1]:
        return jsonify({"error": "Invalid email"}), 400
    # if not email or not EMAIL_RE.match(email):
    #     return jsonify({"error": "Invalid email"}), 400
    if not password or len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    hashed_password = generate_password_hash(password)
    user = User(email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "email": user.email}), 201


# @auth_routes.route("/login", methods=["POST"])
# def login():
#     data = request.get_json() or {}
#     email = data.get("email")
#     password = data.get("password")

#     if not email or not password:
#         return jsonify({"error": "Email and password required"}), 400

#     user = User.query.filter_by(email=email).first()
#     if user and check_password_hash(user.password, password):
#         login_user(user)  # Flask-Login handles session creation
#         return jsonify({"message": "Login successful", "id": user.id, "email": user.email}), 200

    # return jsonify({"error": "Invalid credentials"}), 401

@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    # If GET request, render HTML form
    if request.method == "GET":
        return render_template("login.html")

    # POST request handling
    data = request.get_json() if request.is_json else request.form
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        if request.is_json:
            return jsonify({"error": "Email and password required"}), 400
        return render_template("login.html", error="Email and password required")

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        if request.is_json:
            return jsonify({"message": "Login successful", "id": user.id, "email": user.email}), 200
        return redirect(url_for("task_routes.list_tasks"))

    if request.is_json:
        return jsonify({"error": "Invalid credentials"}), 401
    return render_template("login.html", error="Invalid email or password")
    
@auth_routes.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

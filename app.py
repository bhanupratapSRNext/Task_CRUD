import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from blueprint.auth_routes import auth_routes
from blueprint.task_routes import task_routes
from errors import register_error_handlers
from dotenv import load_dotenv
from flask_login import LoginManager
from extensions import db, migrate, jwt
from flasgger import Swagger

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///taskmanager.db')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret')
    app.config['SWAGGER'] = {
        'title': 'Task Manager API',
        'uiversion': 3,
    }

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
 
    Swagger(app)

    register_error_handlers(app)

    API_VERSION = os.getenv('API_VERSION', 'v1')

    app.register_blueprint(auth_routes, url_prefix=f"/{API_VERSION}/")
    app.register_blueprint(task_routes, url_prefix=f"/{API_VERSION}/")

    @app.route('/health')
    def health():
        return jsonify({"status": "ok"})   

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)

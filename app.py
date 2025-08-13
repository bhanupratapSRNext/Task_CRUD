from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
import os
from blueprint.auth_routes import auth_routes
from blueprint.task_routes import task_routes

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskmanager.db'
app.config['SECRET_KEY'] = 'your_secret_key'

API_VERSION = os.getenv("API_VERSION", "v1")
db.init_app(app)

with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(auth_routes, url_prefix=f"/{API_VERSION}/")
app.register_blueprint(task_routes, url_prefix=f"/{API_VERSION}/")




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True )

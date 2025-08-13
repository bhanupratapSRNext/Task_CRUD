from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from blueprint.auth_routes import auth_routes
from blueprint.task_routes import task_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskmanager.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

# Register blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(task_routes)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True )

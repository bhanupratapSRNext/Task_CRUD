from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime) 

    # Enums for status
    status = db.Column(
        db.String(10),
        nullable=False,
        default='todo' 
    )
    # Enums for priority
    priority = db.Column(
        db.String(10),
        nullable=False,
        default='normal' 
    )
    created_at = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
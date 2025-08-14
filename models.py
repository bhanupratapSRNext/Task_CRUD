# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime


# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)

# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.Text)
#     due_date = db.Column(db.DateTime) 

#     # Enums for status
#     status = db.Column(
#         db.String(10),
#         nullable=False,
#         default='todo' 
#     )
#     # Enums for priority
#     priority = db.Column(
#         db.String(10),
#         nullable=False,
#         default='normal' 
#     )
#     created_at = db.Column(db.DateTime)
#     owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)



from datetime import datetime
from flask_login import UserMixin
from extensions import db
import enum

class StatusEnum(str, enum.Enum):
    todo = 'todo'
    doing = 'progress'
    done = 'done'

class PriorityEnum(str, enum.Enum):
    low = 'low'
    normal = 'medium'
    high = 'high'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)

    tasks = db.relationship('Task', back_populates='owner')

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.todo)
    priority = db.Column(db.Enum(PriorityEnum), nullable=False, default=PriorityEnum.normal)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    owner = db.relationship('User', back_populates='tasks')
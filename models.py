# models.py

import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, organizer, admin
    status = db.Column(db.String(20), default='active')  # active, banned
    verified_organizer = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    photos = db.Column(db.Text)  # Comma-separated image filenames
    status = db.Column(db.String(20), default='active')  # active, cancelled, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RSVP(db.Model):
    __tablename__ = 'rsvps'
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    event_id = db.Column(db.String, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    num_guests = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class AdminAction(db.Model):
    __tablename__ = 'admin_actions'
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    admin_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    action_type = db.Column(db.String(30))  # approve, reject, flag, ban, verify_organizer
    target_id = db.Column(db.String)  # Can be event or user UUID
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class EventHistory(db.Model):
    __tablename__ = 'event_history'
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    event_id = db.Column(db.String, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(30))  # Created, Updated, Deleted, RSVPd
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

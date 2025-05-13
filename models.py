from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<User {self.username}>"

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Admin {self.username}>"

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    race = db.Column(db.String(20), nullable=False)
    character_class = db.Column(db.String(20), nullable=False)
    element = db.Column(db.String(20), nullable=False)
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    gold = db.Column(db.Integer, default=0)
    karma = db.Column(db.Integer, default=0)
    strength = db.Column(db.Integer, default=0)
    agility = db.Column(db.Integer, default=0)
    intelligence = db.Column(db.Integer, default=0)
    endurance = db.Column(db.Integer, default=0)
    rank = db.Column(db.String(2), default="G")
    is_deity = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Player {self.username} (Lvl {self.level} {self.race} {self.character_class})>"

from models.database import db
from datetime import datetime
import secrets

class Roadmap(db.Model):
    __tablename__ = 'roadmaps'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    topic = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(20), default='Beginner')
    estimated_weeks = db.Column(db.Integer)
    share_token = db.Column(db.String(100), unique=True, default=lambda: secrets.token_urlsafe(16))
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    nodes = db.relationship('Node', backref='roadmap', lazy=True, cascade='all, delete-orphan')

class Node(db.Model):
    __tablename__ = 'nodes'

    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000))
    node_order = db.Column(db.Integer)
    difficulty = db.Column(db.String(20))
    estimated_hours = db.Column(db.Integer)
    parent_node_id = db.Column(db.Integer, nullable=True)

    resources = db.relationship('Resource', backref='node', lazy=True, cascade='all, delete-orphan')

class Resource(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    title = db.Column(db.String(200))
    url = db.Column(db.String(500))
    resource_type = db.Column(db.String(50))
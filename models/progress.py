from models.database import db
from datetime import datetime

class Progress(db.Model):
    __tablename__ = 'progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    status = db.Column(db.String(20), default='pending')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class QuizResult(db.Model):
    __tablename__ = 'quiz_results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    score = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
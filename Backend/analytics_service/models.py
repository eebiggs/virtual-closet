from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UsageStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)  # Action taken (e.g., 'item_added')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of the action
    user_id = db.Column(db.Integer, nullable=False)  # User who performed the action

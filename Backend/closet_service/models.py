from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(50))
    color = db.Column(db.String(20))
    season = db.Column(db.String(20))
    user_id = db.Column(db.Integer, nullable=False)  # Associate each item with a user

    def __init__(self, name, category, color, season, user_id):
        self.name = name
        self.category = category
        self.color = color
        self.season = season
        self.user_id = user_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'color': self.color,
            'season': self.season,
            'user_id': self.user_id  # Include user_id in the serialized output
        }

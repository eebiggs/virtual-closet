from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests, os
from datetime import datetime
from models import db, Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath("instance/closet.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")

ANALYTICS_SERVICE_URL = 'http://127.0.0.1:5003'

def track_action(action, user_id):
    tracking_data = {
        'action': action,
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': user_id
    }
    try:
        response = requests.post(f'{ANALYTICS_SERVICE_URL}/track_action', json=tracking_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error tracking action: {e}")

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Virtual Closet API!"})

@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    new_item = Item(
        name=data['name'],
        category=data['category'],
        color=data['color'],
        season=data['season'],
        user_id=user_id  # Ensure user_id is stored
    )
    db.session.add(new_item)
    db.session.commit()

    track_action('item_added', user_id)

    return jsonify({"message": "Item added successfully!"}), 201


@app.route('/items', methods=['GET'])
def get_items():
    user_id = request.args.get('user_id')  # Retrieve the user_id from query params
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    items = Item.query.filter_by(user_id=user_id).all()
    return jsonify([item.to_dict() for item in items])


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    item = Item.query.get(item_id)
    if not item or item.user_id != user_id:
        return jsonify({"error": "Item not found or unauthorized"}), 404

    item.name = data.get('name', item.name)
    item.category = data.get('category', item.category)
    item.color = data.get('color', item.color)
    item.season = data.get('season', item.season)
    db.session.commit()

    track_action('item_updated', user_id)

    return jsonify({"message": "Item updated successfully!"})

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    item = Item.query.get(item_id)
    if not item or item.user_id != user_id:
        return jsonify({"error": "Item not found or unauthorized"}), 404

    db.session.delete(item)
    db.session.commit()

    track_action('item_removed', user_id)

    return jsonify({"message": "Item deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

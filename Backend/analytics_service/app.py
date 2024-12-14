from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from models import db, UsageStats

app = Flask(__name__)
CORS(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Analytics Service API!"}), 200

# Endpoint to track an action
@app.route("/track_action", methods=["POST"])
def track_action():
    try:
        data = request.json
        action = data.get("action")
        user_id = data.get("user_id")
        timestamp = datetime.utcnow()

        if not action or not user_id:
            return jsonify({"error": "Action and user_id are required"}), 400

        new_stat = UsageStats(action=action, timestamp=timestamp, user_id=user_id)
        db.session.add(new_stat)
        db.session.commit()

        return jsonify({"message": "Action tracked successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to retrieve user stats in aggregated format
@app.route("/user_stats", methods=["GET"])
def get_user_stats():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        actions = UsageStats.query.filter_by(user_id=user_id).all()

        if not actions:
            # If no actions for this user, return all zero and no last_updated
            return jsonify({
                "added": 0,
                "removed": 0,
                "updated": 0,
                "last_updated": None
            }), 200

        added_count = sum(1 for a in actions if a.action == "item_added")
        removed_count = sum(1 for a in actions if a.action == "item_removed")
        updated_count = sum(1 for a in actions if a.action == "item_updated")

        last_timestamp = max(a.timestamp for a in actions)
        last_timestamp_str = last_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return jsonify({
            "added": added_count,
            "removed": removed_count,
            "updated": updated_count,
            "last_updated": last_timestamp_str
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to retrieve all actions
@app.route("/all_actions", methods=["GET"])
def get_all_actions():
    try:
        actions = UsageStats.query.all()
        result = [
            {
                "user_id": action.user_id,
                "action": action.action,
                "timestamp": action.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
            for action in actions
        ]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clear_logs", methods=["DELETE"])
def clear_logs():
    try:
        num_deleted = db.session.query(UsageStats).delete()
        db.session.commit()

        return jsonify({"message": f"All logs cleared. {num_deleted} records deleted."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5003)

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from config import AUTH_SERVICE_URL, CLOSET_SERVICE_URL, ANALYTICS_SERVICE_URL

app = Flask(__name__)
CORS(app)  # Enable CORS globally

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        response = requests.post(f"{AUTH_SERVICE_URL}/register", json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        print(f"Received login request: {data}")  # Log the incoming request

        # Forward request to Auth Service
        response = requests.post(f"{AUTH_SERVICE_URL}/login", json=data)
        print(f"Auth service response status: {response.status_code}")  # Log status code
        print(f"Auth service response body: {response.json()}")  # Log response JSON

        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"Error in /login route: {str(e)}")  # Log any exceptions
        return jsonify({"error": str(e)}), 500

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    try:
        data = request.json
        response = requests.delete(f"{AUTH_SERVICE_URL}/delete_user", json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        response = requests.get(f"{AUTH_SERVICE_URL}/users")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/items', methods=['POST'])
def add_item():
    try:
        data = request.json
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        closet_response = requests.post(f"{CLOSET_SERVICE_URL}/items", json=data)
        if closet_response.status_code == 201:
            analytics_data = {
                "action": "item_added",
                "user_id": user_id,
                "timestamp": data.get("timestamp")
            }
            requests.post(f"{ANALYTICS_SERVICE_URL}/track_action", json=analytics_data)
        return jsonify(closet_response.json()), closet_response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/items', methods=['GET'])
def get_items():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        response = requests.get(f"{CLOSET_SERVICE_URL}/items", params={"user_id": user_id})
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        data = request.json
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        response = requests.put(f"{CLOSET_SERVICE_URL}/items/{item_id}", json=data)
        
        # If the item was successfully updated (status 200), log 'item_updated' action
        if response.status_code == 200:
            analytics_data = {
                "action": "item_updated",
                "user_id": user_id,
                "timestamp": data.get("timestamp") or ""
            }
            requests.post(f"{ANALYTICS_SERVICE_URL}/track_action", json=analytics_data)

        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        data = request.json
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        response = requests.delete(f"{CLOSET_SERVICE_URL}/items/{item_id}", json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analytics', methods=['GET'])
def get_analytics():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        response = requests.get(f"{ANALYTICS_SERVICE_URL}/user_stats", params={"user_id": user_id})
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/all_actions', methods=['GET'])
def get_all_actions():
    try:
        response = requests.get(f"{ANALYTICS_SERVICE_URL}/all_actions")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clear_logs', methods=['DELETE'])
def clear_logs():
    try:
        response = requests.delete(f"{ANALYTICS_SERVICE_URL}/clear_logs")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5005, debug=True)



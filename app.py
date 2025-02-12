from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from datetime import datetime

app = Flask(__name__)
CORS(app)


client = MongoClient("mongodb://127.0.0.1:27017")
db = client["users"]
collection = db["users"]


def transform_user(user):
    user["_id"] = str(user["_id"])
    return user


@app.route("/api/users", methods=["GET"])
def get_users():
    users = list(collection.find({}))
    return jsonify([transform_user(user) for user in users])


@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        abort(404)
    user["_id"] = str(user["_id"])
    return jsonify(user)


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json

    user = {
        "username": data["username"],
        "password": data["password"],
        "roles": data["roles"],
        "preferences": data["preferences"],
        "active": data.get("active", True),
        "created_ts": datetime.utcnow().timestamp(),
        "last_updated_ts": datetime.utcnow().timestamp(),
    }
    result = collection.insert_one(user)
    return jsonify({"id": str(result.inserted_id)})


@app.route("/api/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    print(data)
    updated_user = {
        "username": data["username"],
        "password": data["password"],
        "roles": data["roles"],
        "preferences": data["preferences"],
        "active": data["active"],
        "last_updated_ts": datetime.utcnow().timestamp(),
    }
    result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})
    if result.matched_count == 0:
        abort(404)
    return jsonify({"message": "User updated successfully"})


@app.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        abort(404)
    return jsonify({"message": "User deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)

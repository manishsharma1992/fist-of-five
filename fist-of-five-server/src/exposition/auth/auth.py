from flask import Blueprint, jsonify, request

from src.exposition.auth.dto.dto import RegisterUserRequest

blueprint = Blueprint("users", __name__, url_prefix="/api/users")

@blueprint.route("/login-user", methods=["POST"])
def login_user():
    data = request.get_json()
    print(data)
    return jsonify({"message": "User logged in successfully"}), 200


@blueprint.route("/register-user", methods=["POST"])
def register_user():
    data = request.get_json(force=True)
    print(data)
    req = RegisterUserRequest(
        uid=data["uid"],
        first_name=data["firstName"],
        last_name=data["lastName"],
        password=data["password"]
    )
    return jsonify({"message": "User registered successfully"}), 200

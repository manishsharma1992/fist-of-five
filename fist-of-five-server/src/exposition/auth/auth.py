from flask import Blueprint, jsonify, request

blueprint = Blueprint("users", __name__, url_prefix="/api/users")

@blueprint.route("/register-user", methods=["POST"])
def register_user():
    data = request.get_json()
    return jsonify({"message": "User registration endpoint"}), 200
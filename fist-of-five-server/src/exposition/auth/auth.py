from flask import Blueprint, jsonify, request

from src.domain.auth.service.auth_service import AuthService
from src.management.auth.auth_management import AuthManagement

blueprint = Blueprint("users", __name__, url_prefix="/api/users")
auth_service = AuthService()
auth_management = AuthManagement(auth_service)

@blueprint.route("/register-user", methods=["POST"])
def register_user():
    data = request.get_json()
    user = auth_management.register_user(data)
    return jsonify({"message": "User registered successfully"}), 200
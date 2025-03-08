# src/management/auth/auth_management.py
from src.domain.auth.service.auth_service import AuthService


class AuthManagement:
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    def register_user(self, user_data: dict):
        return self._auth_service.create_user(
            username=user_data.get('username'),
            password=user_data.get('password'),
            created_by=user_data.get('created_by', 'system'),
            updated_by=user_data.get('updated_by', 'system')
        )

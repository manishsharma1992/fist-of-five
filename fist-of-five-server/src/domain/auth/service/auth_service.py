# src/domain/auth/service/auth_service.py
from src.domain.auth.models import User
from src.infrastructure import db


class AuthService:
    def create_user(self, username: str, password: str, created_by: str, updated_by: str) -> User:
        user = User(
            username=username,
            password=password,  # Note: In production, password should be hashed
            created_by=created_by,
            updated_by=updated_by
        )
        db.session.add(user)
        db.session.commit()
        return user
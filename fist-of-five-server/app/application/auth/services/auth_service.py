from datetime import datetime, UTC

from fastapi import HTTPException, status

from app.application.auth.dtos import RegisterRequest, RegisterResponse
from app.domain.auth import User
from app.infrastructure.repositories.auth import UserRepository, RoleRepository
from app.infrastructure.security.password import hash_password


class AuthService:

    def __init__(
            self,
            user_repository: UserRepository,
            role_repository: RoleRepository
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def register(self, request: RegisterRequest) -> RegisterResponse:
        """
        Register a new user.

        Business Logic:
        1. Check if UID already exists → raise error
        2. Check if email already exists → raise error
        3. Hash the password
        4. Create User object
        5. Assign role to user
        6. Save user
        7. Return success response

        Args:
            request: Registration request data

        Returns:
            RegisterResponse with success message

        Raises:
            HTTPException: If UID or email already exists
        """
        if self.user_repository.exists_by_uid(request.uid):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Employee ID {request.uid} is already registered"
            )

        if self.user_repository.exists_by_email(str(request.email)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {request.email} is already registered"
            )

        password_hash = hash_password(request.password)

        user = User(
            uid=request.uid,
            email=request.email,
            password_hash=password_hash,
            first_name=request.first_name,
            last_name=request.last_name,
            middle_name=request.middle_name,
            active=True,
            created_at=datetime.now(UTC),
            modified_at=datetime.now(UTC)
        )

        role = self.role_repository.find_by_name(request.role.value)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Role {request.role.value} not found in database"
            )

        user.roles.append(role)

        saved_user = self.user_repository.save(user)

        return RegisterResponse(
            message="Registration successful. Please login to continue.",
            uid=saved_user.uid,
            email=saved_user.email
        )

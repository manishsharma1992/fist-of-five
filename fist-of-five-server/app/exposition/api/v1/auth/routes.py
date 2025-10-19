from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application import RegisterResponse, RegisterRequest
from app.application.auth import AuthService
from app.infrastructure.connection import get_db
from app.infrastructure.repositories import UserRepository, RoleRepository

router = APIRouter()

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Factory for UserRepository"""
    return UserRepository(db)

def get_role_repository(db: Session = Depends(get_db)) -> RoleRepository:
    """Factory for RoleRepository"""
    return RoleRepository(db)

def get_auth_service(
        user_repo: UserRepository = Depends(get_user_repository),
        role_repo: RoleRepository = Depends(get_role_repository)
) -> AuthService:
    """Factory for AuthService"""
    return AuthService(user_repo, role_repo)

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registered a new user",
    description="Register a new user with employee ID, email, and role selection"
)
def register(
        request: RegisterRequest,
        auth_service: AuthService = Depends(get_auth_service)
) -> RegisterResponse:
    """
    Register a new user for Planning Poker.

    - **uid**: Employee ID (format: letter + 5 digits, e.g., f93328)
    - **email**: Corporate email (@bnpparibas.com)
    - **password**: Secure password (min 8 chars, uppercase, lowercase, digit)
    - **role**: observer or estimator
    """
    return auth_service.register(request)
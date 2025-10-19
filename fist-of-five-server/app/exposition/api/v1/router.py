from fastapi import APIRouter
from .auth.routes import router as auth_router

# Create main v1 router
api_v1_router = APIRouter(prefix="/api/v1")

# Include auth routes
api_v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
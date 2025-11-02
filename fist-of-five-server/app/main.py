from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.exposition.api.v1.router import api_v1_router

app = FastAPI(
    title="Planning Poker API",
    description="Agile Planning Poker & Capacity Planning Tool",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Angular dev server
        "http://127.0.0.1:4200",  # Alternative localhost
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  # Allow all headers
)

# Register routers
app.include_router(api_v1_router)
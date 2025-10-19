from fastapi import FastAPI
from app.exposition.api.v1.router import api_v1_router

app = FastAPI(
    title="Planning Poker API",
    description="Agile Planning Poker & Capacity Planning Tool",
    version="1.0.0"
)

# Register routers
app.include_router(api_v1_router)

@app.get("/")
def root():
    return {"message": "Welcome to Planning Poker API"}
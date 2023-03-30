
from api.endpoints import statistic
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(
    statistic.router, prefix="/statistics", tags=["statistics"])

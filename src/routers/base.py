from fastapi import FastAPI, APIRouter
import os


base_router = APIRouter()


@base_router.get("/")
async def welcome():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    return {
        "message": "Welcome to the RAG app",
        "app_name": app_name,
        "app_version": app_version
    }

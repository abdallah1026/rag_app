from fastapi import FastAPI, APIRouter, Depends
import os
from helper.config import get_settings


base_router = APIRouter()


@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):

    return {
        "message": "Welcome to the RAG app",
        "app_name": app_settings.APP_NAME,
        "app_version": app_settings.APP_VERSION
    }

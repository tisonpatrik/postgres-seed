from fastapi import FastAPI
from src.api.router import router
from src.core.config import settings

import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    root_path=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.include_router(router, prefix=settings.api_prefix)

@app.get("/")
async def root():
    return {"Ping": "Pong!"}
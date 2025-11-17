from fastapi import FastAPI

from app.router import router

app = FastAPI(
    openapi_url="/openapi.json",
    docs_url="/",
)

app.include_router(router)
    
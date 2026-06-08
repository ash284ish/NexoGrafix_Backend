from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routes import api_router
from app.core.config import settings

app = FastAPI(
    title="Nexografix CMS Backend"
)

# Lock CORS origins: wildcard + allow_credentials=True is rejected by browsers
_allowed_origins = ["https://nexografix.com", "https://www.nexografix.com"]
if settings.ENV != "production":
    _allowed_origins += ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response

BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "app" / "public" / "uploads"

app.mount(
    "/api/uploads",
    StaticFiles(directory=str(UPLOADS_DIR)),
    name="api_uploads"
)

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOADS_DIR)),
    name="uploads"
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api/v1")

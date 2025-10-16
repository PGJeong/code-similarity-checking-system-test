from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from .config import load_settings
from .database import get_db

settings = load_settings()

app = FastAPI()

# CORS
origins = [settings.CORS_FRONTEND]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to 「Code Similarity Checking System」 API Server"}


from .routes.auth import auth
app.include_router(auth.router)

from .routes.license_repository import license_repository
app.include_router(license_repository.router)

from .routes.pr_log import pr_log
app.include_router(pr_log.router)

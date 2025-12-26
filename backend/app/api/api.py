from fastapi import APIRouter, FastAPI, Depends
from app.api.v1.routers import auth


app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["auth"])





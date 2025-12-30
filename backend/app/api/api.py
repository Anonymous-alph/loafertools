from fastapi import APIRouter, FastAPI, Depends
from app.api.v1.routers import auth, focus_session


app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(focus_session.router, prefix="/focussession", tags=["focussession"] )





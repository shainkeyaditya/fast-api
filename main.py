import sys
sys.path.append("..")
from fastapi import FastAPI, Depends, status, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
from routers import routes
from database import Base, SessionLocal, engine
appPort = FastAPI(
    title="Innomick fast api docs",
    description="This API was built with FastAPI and exists to find related blog articles given the ID of blog article.",
    version="1.0.0",
    servers=[
        {"url": "http://localhost:8000", "description": "Development Server"},
        {
            "url": "https://mock.pstmn.io",
            "description": "Mock Server",
        },
    ],
)
appPort.include_router(routes.router)
fakeDb = []
db = SessionLocal()
router = APIRouter()
Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Course(BaseModel):
    id: int
    name: str
    price: float
    is_early_bird: Optional[bool] = None


class UserSchema(BaseModel):  # serializers
    username: str
    email: str
    password: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class Item(BaseModel):  # serializer
    id: int
    name: str
    description: str
    price: int
    on_offer: Optional[bool] = None

    class Config:
        orm_mode = True


@appPort.get("/")
def read_root() -> str:
    return {"greetings": "Welcome to fast api tutorial"}

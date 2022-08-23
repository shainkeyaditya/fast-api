from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from models import Users
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


appPort = FastAPI(
    title="Upaway api docs",
    description="This API was built with FastAPI and exists to find related blog articles given the ID of blog article.",
    version="1.0.0",
servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development Server"
        },
        {
            "url": "https://mock.pstmn.io",
            "description": "Mock Server",
        }
    ],
)
fakeDb = []


class Course(BaseModel):
    id: int
    name: str
    price: float
    is_early_bird: Optional[bool] = None


class UserSchema(BaseModel):
    name: str
    email: str
    class Config:
        orm_mode = True


@appPort.get('/')
def read_root():
    return {
        "greetings": "Welcome to fast api tutorial"
    }


@appPort.get("/course")
def get_courses():
    return fakeDb


@appPort.get("/courses/{course_id}")
def get_a_course(course_id: int):
    course = course_id - 1
    return fakeDb[course]


@appPort.post("/courses")
def add_course(course: Course):
    fakeDb.append(course.dict())
    return fakeDb[-1]


@appPort.delete("/courses/{course_id}")
def delete_course(course_id: int):
    fakeDb.pop(course_id-1)
    return {
        "task": "Deletion successful"
    }


@appPort.get("/users",response_model=List[UserSchema])
def get_users(db:Session=Depends(get_database_session)):
    return db.query(Users).all()



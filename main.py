from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List

import models
from models import Users
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

# def get_database_session():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()

x = [{"x": 1}]

appPort = FastAPI(
    title="Upaway api docs",
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
fakeDb = []
db = SessionLocal()


class Course(BaseModel):
    id: int
    name: str
    price: float
    is_early_bird: Optional[bool] = None


class UserSchema(BaseModel):  # serializers
    name: str
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
def read_root():
    return {"greetings": "Welcome to fast api tutorial"}


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
    fakeDb.pop(course_id - 1)
    return {"task": "Deletion successful"}


# @appPort.get("/users", response_model=List[UserSchema])
# def get_users(db: Session = Depends(get_database_session)):
#     return db.query(Users).all()


@appPort.post("/users", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSchema):
    db_item = (
        db.query(models.UserSchema).filter(models.UserSchema.name == user.name).first()
    )

    if db_item is not None:
        raise HTTPException(status_code=400, detail="Item already exists")
    new_user = models.Users(
        name=user.name,
        email=user.email,
        password=user.password,
        created_at="",
        updated_at="",
    )
    db.add(new_user)
    db.commit()
    return {"status": 201, "transaction": "Successful"}


@appPort.get("/items", response_model=List[Item], status_code=200)
def get_all_items():
    items = db.query(models.Item).all()

    return items


@appPort.get("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_an_item(item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return item


@appPort.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_an_item(item: Item) -> dict:
    """

    :param item:
    :return: dictionat that giving the item response
    """
    db_item = db.query(models.Item).filter(models.Item.name == item.name).first()

    if db_item is not None:
        raise HTTPException(status_code=400, detail="Item already exists")

    new_item = models.Item(
        name=item.name,
        price=item.price,
        description=item.description,
        on_offer=item.on_offer,
    )

    db.add(new_item)
    db.commit()

    return new_item


@appPort.put("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def update_an_item(item_id: int, item: Item):
    """

    :param item_id: int
    :param item: name
    :return: json
    """
    item_to_update = db.query(models.Item).filter(models.Item.id == item_id).first()
    item_to_update.name = item.name
    item_to_update.price = item.price
    item_to_update.description = item.description
    item_to_update.on_offer = item.on_offer

    db.commit()

    return item_to_update


@appPort.delete("/item/{item_id}")
def delete_item(item_id: int) -> str:
    """

    :param item_id: id
    :return: str
    """
    item_to_delete = db.query(models.Item).filter(models.Item.id == item_id).first()

    if item_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found"
        )

    db.delete(item_to_delete)
    db.commit()

    return "Deleted Successfully"


# we can make async call like this one
async def fetch_from_database():
    return {"status": "Ok"}


async def get_results():
    return await fetch_from_database()


@appPort.get("/request")
async def read_results():
    results = await get_results()
    return results

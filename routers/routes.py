from fastapi import Depends, status, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional, List
import models
from database import SessionLocal, engine
from passlib.context import CryptContext
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={401: {"user": "Not authorized"}}
)

x = [{"x": 1}]
fakeDb = []
db = SessionLocal()
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
# router = APIRouter()


class Course(BaseModel):
    id: int
    name: str
    price: float
    is_early_bird: Optional[bool] = None


class UserSchema(BaseModel):  # serializers
    name: str
    email: str
    password: str
    # created_at: str
    # updated_at: str

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


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return bcrypt_context.hash(password)

@router.get("/")
def read_root():
    return {"greetings": "Welcome to fast api tutorial"}


@router.get("/course")
def get_courses():
    return fakeDb


@router.get("/courses/{course_id}")
def get_a_course(course_id: int):
    course = course_id - 1
    return fakeDb[course]


@router.post("/courses")
def add_course(course: Course):
    fakeDb.append(course.dict())
    return fakeDb[-1]


@router.delete("/courses/{course_id}")
def delete_course(course_id: int):
    fakeDb.pop(course_id - 1)
    return {"task": "Deletion successful"}


# @router.get("/users", response_model=List[UserSchema])
# def get_users(db: Session = Depends(get_database_session)):
#     return db.query(Users).all()


@router.post("/create/users", )
async def create_user(create_user: UserSchema, db: Session = Depends(get_db)) -> dict:
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.name = create_user.name
    hash_pass = get_password_hash(create_user.password)
    create_user_model.password = hash_pass
    db.add(create_user_model)
    db.commit()
    return create_user_model


@router.get("/items", response_model=List[Item], status_code=200)
def get_all_items():
    items = db.query(models.Item).all()

    return items


@router.get("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_an_item(item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return item


@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
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


@router.put("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
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


@router.delete("/item/{item_id}")
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


@router.get("/request")
async def read_results():
    results = await get_results()
    return results

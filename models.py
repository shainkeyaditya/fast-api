from database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    created_at = Column(String(100))
    updated_at = Column(String(100))

    def __repr__(self):
        return f"<name and email ={self.name}{self.email}>"


class JobType(Base):
    __tablename__ = "job_type"

    id = Column(Integer, primary_key=True, index=True)


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    on_offer = Column(Boolean, default=False)
    # owner = relationship("Users", back_populates="items")

    def __repr__(self):
        return f"<Item name={self.name} price={self.price}>"

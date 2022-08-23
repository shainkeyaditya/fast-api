from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DB_URL = "mysql://root:root@127.0.0.1:3306/fastapidemo"
DB_URL = "mysql+mysqlconnector://root:test@localhost:3306/fastapidb"
'''
Its provides a nice “Pythonic” way of interacting with databases
Asynchronous Server Gateway interface

'''

engine = create_engine(DB_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, bind=engine)
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_table'

    id = Column(String(20), primary_key=True)
    username = Column(String(20))
    password = Column(String(100))

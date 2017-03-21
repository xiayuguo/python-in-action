from sqlalchemy import Column, String, Integer
from db import Base, CRUDMixin


class User(Base):
    __tablename__ = 'user_table'

    id = Column(String(20), primary_key=True)
    username = Column(String(20))
    password = Column(String(100))


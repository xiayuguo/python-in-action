# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


"""
# default
engine = create_engine('mysql://scott:tiger@localhost/foo')

# mysql-python
engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')

# MySQL-connector-python
engine = create_engine('mysql+mysqlconnector://scott:tiger@localhost/foo')

# OurSQL
engine = create_engine('mysql+oursql://scott:tiger@localhost/foo')

For more details, please visit:
    http://docs.sqlalchemy.org/en/latest/core/engines.html?highlight=create_engine

"""

engine = create_engine('mysql+pymysql://username:password@localhost:3306/database')

Session = sessionmaker(bind=engine, autocommit=True)

db = Session()
Base = declarative_base()


class CRUDMixin(object):
    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    def update(self):
        """Saves the object to the database."""
        db.commit()
        return self

    def save(self):
        """Saves the object to the database."""
        db.add(self)
        db.commit()
        return self

    def delete(self):
        """Delete the object from the database."""
        db.delete(self)
        db.commit()
        return self

    @classmethod
    def clear(cls):
        """Delete all datas form database"""
        db.query(cls).delete()
        db.commit()



class Transaction(object):
    """get a connection and do something in transaction"""
    global db

    def __enter__(self):
        db.autocommit = False
        return db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            db.rollback()
            print(u"事务执行失败,回滚")
        else:
            db.commit()
            print(u"事务执行成功,提交")

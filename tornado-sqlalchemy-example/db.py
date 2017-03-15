# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

engine = create_engine('mysql+pymysql://root:h@localhost:3306/irain_park')

Session = sessionmaker(bind=engine, autocommit=True)

db = Session()


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

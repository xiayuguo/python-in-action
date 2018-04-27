import redis
import pymysql

from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor


class Pool(object):
    def __init__(self, host, port, user, password, db, charset='utf8', *args, **kwargs):
        self.pool = PooledDB(
            pymysql,
            50,
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=db,
            charset=charset,
            setsession=['SET AUTOCOMMIT = 1']
        )

    def get_conn(self):
        return self.pool.connection()

    def put_conn(self, conn):
        conn.close()

    def select(self, sql, params=None):
        """execute a select sql"""
        # print("This SQL will be execute:\n%s" % sql)
        conn = self.get_conn()
        # conn.autocommit(1)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return_list = cursor.fetchall()
        cursor.close()
        self.put_conn(conn)
        return return_list

    def select_row(self, sql, *args, **kwargs):
        """execute a select sql and return the first row"""
        result = self.select(sql, *args, **kwargs)
        if result:
            return result[0]
        else:
            return None

    def select_dict(self, sql, *args, **kwargs):
        """execute a select sql and return a dict , column name is the keys"""
        print("This SQL will be execute:\n%s" % sql)
        conn = self.get_conn()
        # conn.autocommit(1)
        cursor = conn.cursor(DictCursor)
        cursor.execute(sql, *args, **kwargs)
        if cursor.rowcount >= 1:
            row_count = str(cursor.rowcount)
        else:
            row_count = 'No'
        print("%s rows fetched." % row_count)
        return_list = cursor.fetchall()
        cursor.close()
        self.put_conn(conn)
        return return_list

    def select_row_dict(self, sql, *args, **kwargs):
        """execute a select sql and return the first row"""
        result = self.select_dict(sql, *args, **kwargs)
        if result:
            return result[0]
        else:
            return None

    def do(self, sql, *args, **kwargs):
        """execute a non-select sql"""
        print("This SQL will be execute:\n%s" % sql)
        conn = self.get_conn()
        # conn.autocommit(1)
        cursor = conn.cursor()
        cursor.execute(sql, *args, **kwargs)
        if cursor.rowcount >= 1:
            row_count = str(cursor.rowcount)
        else:
            row_count = 'No'
        print("%s rows changed." % row_count)
        cursor.close()
        self.put_conn(conn)
        return None

    # TODO 判断结果有效性
    def get_value(self, sql, *args, **kwargs):
        """if select one row one cloumn, return a value"""
        result = self.select_row(sql, *args, **kwargs)
        if result:
            return result[0]
        else:
            return None

    def get_list(self, sql, *args, **kwargs):
        """if select one column,return as a line tuple"""
        result = self.select(sql, *args, **kwargs)
        if result:
            return [line[0] for line in result]
        else:
            return list()

    def get_dict(self, sql, *args, **kwargs):
        """if select two column,return a dict,the 1st col is key"""
        result = self.select(sql, *args, **kwargs)
        if result:
            return {line[0]: line[1] for line in result}
        else:
            return dict()


class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db= redis.StrictRedis(**redis_kwargs)
        self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)
        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)


redisdb = RedisQueue(
    name='test',
    host='127.0.0.1',
    port=6379,
    db=0
)

db = pymysql.connect(host="127.0.0.1", user="root", password="****", database="****", port=3306)

db_pool = Pool(host="127.0.0.1", user="root", password="****", db="***", port=3306)


def select(sql, is_pool=True):
    """简单的查询"""
    if is_pool:
        return db_pool.select(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    return data
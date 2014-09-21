#-*- coding=utf-8 -*-

#from codedim import  return_code_dim
from DBUtils.PooledDB import PooledDB
from types import *
import psycopg2
import psycopg2.extras
import sys

db_params = {  # DBUtils 连接池参数
    'creator': psycopg2,
    'host': 'localhost',
    'user': 'postgres',
    'password': '123456',
    'database': 'jf_card',
    'failures': (psycopg2.IntegrityError)
}

pool = PooledDB(maxusage=1000, **db_params)  # 创建连接池


class DB:
    def __init__(self):
        self.connection = pool.connection()  # 从连接池中获取一个连接

    def _fetch_data(self, sql, tuple, fetchAll=True):  # 执行SQL语句并返回结果
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql, tuple)
        rst = cursor.fetchall()
        if rst:
            if fetchAll:
                return rst
            else:
                return rst[0]
        else:
            return None

    def fetch_all(self, sql, tuple):
        return self._fetch_data(sql, tuple, True)

    def fetch_one(self, sql, _tuple):
        return self._fetch_data(sql, _tuple, False)

    def execute(self, sql, _tuple=()):
        '''
        执行SQL语句
        '''
        print 'sql--> ', sql % (_tuple)
        print 'sql--> ', sql
        print 'tuple--> ', _tuple
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql, _tuple)
        return True

    def commit(self):
        self.connection.commit()
        self.connection.close()

    def rollback(self):
        self.connection.rollback()
        self.connection.close()

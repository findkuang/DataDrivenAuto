#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/21 17:34
# @Author  : kuangxiaojiang
# @Site    : 
# @File    : MysqlHelper.py
# @Function: 数据库操作
import pymysql
from Utils.GetConfigInfo import DB_INFO
from DB.Singleton import singleton
from Utils.LoggerHandler import logger


@singleton
class MysqlHelper(object):
    def __init__(self, env, db, charset='utf8'):
        if env == 'mysql-dev':
            db_inf = DB_INFO['mysql-dev']
        else:
            db_inf = DB_INFO['mysql-test']
        self.host = db_inf['host']
        self.port = int(db_inf['port'])
        self.db = db
        self.user = db_inf['user']
        self.passwd = db_inf['password']
        self.charset = charset

    def connect(self):
        self.conn = pymysql.Connect(host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd,
                                    charset=self.charset)
        self.cursor = self.conn.cursor(cursor = pymysql.cursors.DictCursor)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self, sql, params=()):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            logger().error(e)
        return result

    def get_all(self, sql, params=()):
        list = []
        try:
            self.connect()
            self.cursor.execute(sql, params)
            list = self.cursor.fetchall()
            self.close()
        except Exception as e:
            logger('数据库查询').error(e)
        if len(list) == 0:
            list = []
        return list

    def insert(self, sql, params=()):
        return self.__edit(sql, params)

    def update(self, sql, params=()):
        return self.__edit(sql, params)

    def delete(self, sql, params=()):
        return self.__edit(sql, params)

    def __edit(self, sql, params):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            logger().error(e)
        return count
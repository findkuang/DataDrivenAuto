#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/6 22:47
# @Author  : kuangxiaojiang
# @File    : DbAPI.py
# @Function: 数据库API
from DB.MysqlHelper import MysqlHelper
import re


def query_db(sql_file, **params):
    '''
    数据库查询api
    :param sql_file: sql文件路径或者sql语句
    :param params: 查询条件
    :return:
    '''
    if 'select' in sql_file:
        sql = sql_file
    else:
        with open(sql_file, encoding='utf-8') as f:
            # 获取第一条SQL
            sql = f.read().split(';')[0]
    sql = sql.format(**params['query']).replace('from', 'FROM')
    # 获取数据库db信息
    db_name = re.findall('.(.+?)\.', sql.split('FROM')[1])[0]
    db = MysqlHelper('mysql-test', db_name)
    query_rst = db.get_all(sql)
    return query_rst


def execute_sql(sql, **params):
    '''
    执行数据库操作，增删改
    :return:
    '''
    sql = sql.format(**params['query']).replace('from', 'FROM')
    # 获取数据库db信息
    db_name = re.findall('.(.+?)\.', sql.split('FROM')[1])[0]
    db = MysqlHelper('mysql-test', db_name)
    if bool(re.search('update', sql, re.IGNORECASE)):
        db.update(sql)
    elif bool(re.search('delete', sql, re.IGNORECASE)):
        db.delete(sql)
    elif bool(re.search('insert', sql, re.IGNORECASE)):
        db.insert(sql)
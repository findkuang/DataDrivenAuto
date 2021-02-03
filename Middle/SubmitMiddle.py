#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 17:12
# @Author  : kuangxiaojiang
# @File    : SubmitMiddle.py
# @Function: 提交类接口中间层
from Common.Login import Login
from Utils.CompareData import compare_data
from Utils.FormatDbRst import get_db_format_data
from DB.DbAPI import query_db
from Utils.GetConfigInfo import URL_INFO
from Utils.LoggerHandler import logger
import json
from Utils.RandomData import RandomData
from Utils.FormatOtherData import format_data_by_setup


def submit_data_and_verify(username, pwd, uri, body, expected_rst, sql_path, yml_path, send_method, **params):
    '''
    提交数据请求后，验证数据库结果
    :param expected_rst: 预期结果
    :param url: 请求url
    :param body: 请求报文
    :param sql_path: sql文件
    :param yml_path: yml格式化文件
    :param send_method: 请求方法
    :return:
    '''
    sql_file = sql_path
    yml_file = yml_path
    # 格式化前置条件传的数据
    setUp_dict = params['setUp']
    body = format_data_by_setup(body, setUp_dict)
    conditions = format_data_by_setup(params['query'], setUp_dict)
    expected_rst = format_data_by_setup(expected_rst, setUp_dict)

    random_obj = RandomData()
    expected_rst = random_obj.get_random_data_value(expected_rst)
    # 登录
    lg = Login(username, pwd)
    req = lg.req
    headers = {"Authorization": 'Bearer '+ lg.access_token,
               "k2": lg.defaultLoc,
               "k1": lg.defaultIns
    }
    # 发送接口请求
    url = URL_INFO['TEST']['url'] + uri
    if send_method == 'POST':
        rst = req.send_post(url, data=body, headers=headers)
    else:
        rst = req.send_get(url, data=body, headers=headers)
    # 数据库查询校验
    # 如果yml配置文件为空，则直接查询数据库,不需要进行格式化
    if yml_path == '':
        db_rst = query_db(sql_file, query=conditions)
        logger('数据库查询结果：').debug(db_rst)
        if len(db_rst) > 0:
            fm_db_rst = json.dumps(db_rst[0])
        else:
            logger('数据库查询结果：').error('数据库查询结果为空')
            fm_db_rst = '{}'
    else:
        fm_db_rst = get_db_format_data(sql_file, yml_file, query=conditions)
        logger('数据库查询结果根据YML格式化为：').debug(fm_db_rst)
    # 数据库查询结果和预期结果比对
    logger('【=====expected_rst预期结果为：=====】').debug(expected_rst)
    logger('【=====数据库需比对数据：=====】').debug(fm_db_rst)
    compare_data(expected_rst, fm_db_rst)
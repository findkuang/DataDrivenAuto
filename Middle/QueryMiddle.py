#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 17:12
# @Author  : kuangxiaojiang
# @File    : QueryMiddle.py
# @Function: 查询类接口中间层

from Common.Login import Login
from Utils.FormatMessage import format_data
from Utils.CompareData import compare_data
from Utils.FormatDbRst import get_db_format_data
from Utils.GetConfigInfo import URL_INFO
from Utils.LoggerHandler import logger
from Utils.FormatOtherData import format_data_by_setup
import json


def get_query_compare_rst(username, pwd, uri, body, expected_rst, sql_file_name, yml_file_name, send_method, **params):
    '''
    接口查询数据并和数据库结果比对
    :param username: 登录用户名
    :param pwd: 登录密码
    :param uri: 请求uri
    :param body: 请求报文
    :param expected_rst: 期望结果
    :param sql_file_name: sql文件
    :param yml_file_name: yml格式化文件
    :param current_dir: 当前目录
    :param send_method: 请求方法
    :return:
    '''
    sql_file = sql_file_name
    yml_file = yml_file_name
    # 格式化前置条件传的数据
    setUp_dict = params['setUp']
    body = format_data_by_setup(body, setUp_dict)
    conditions = format_data_by_setup(params['query'], setUp_dict)
    expected_rst = format_data_by_setup(expected_rst, setUp_dict)

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
    # 接口返回结果格式化
    target_json = format_data(rst, yml_file)
    logger('接口返回结果格式化结果:').debug(target_json)
    # 如果期望结果expected_rst不为空，则不需要查询数据库，直接使用expected_rst与target_json比对
    if expected_rst:
        compare_data(target_json, expected_rst)
    else:
        # 执行数据库查询并返回格式化后的结果
        fm_db_rst = get_db_format_data(sql_file, yml_file, query=conditions)
        logger('数据库查询结果后根据YML格式化:').debug(fm_db_rst)
        # 数据库查询结果和接口返回结果比对
        logger('【=====接口需比对数据：=====】').debug(target_json)
        logger('【=====数据库需比对数据：=====】').debug(fm_db_rst)
        compare_data(target_json, fm_db_rst)

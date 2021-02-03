#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 18:15
# @Author  : kuangxiaojiang
# @File    : RequestApi.py
# @Function:
from Common.Login import Login
from Utils.GetConfigInfo import URL_INFO
import json


def request_api(username, pwd, uri, body, send_method='POST'):
    '''
    HTTP请求API
    :param username: 用户名
    :param pwd: 密码
    :param send_method:请求方法
    :param uri: 接口地址
    :param body: 请求报文
    :return:
    '''
    # 登录
    # body = json.loads(body, encoding='utf-8')
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
    return rst
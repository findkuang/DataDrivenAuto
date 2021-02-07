#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/9 12:49
# @Author  : kuangxiaojiang
# @File    : FormatOtherData.py
# @Function: 格式其他数据
import re
from Utils.LoggerHandler import logger
import jsonpath
import json


def format_body_by_rely(body, rely_data):
    '''
    根据依赖关系格式化请求参数
    :param body:
    :param rely_data:
    :return:
    '''
    if isinstance(body, dict):
        body = json.dumps(body)
    rely_filed_list = re.findall(r'\"(\$.*?)\"', body)
    for rely_filed in rely_filed_list:
        try:
            rely_value = str(jsonpath.jsonpath(rely_data, rely_filed)[0])
            new_body = body.replace(rely_filed, rely_value)
        except Exception as e:
            logger('接口间数据传递').error(rely_filed)
            logger('接口间数据传递').error(e)
        body = new_body
    return body


def format_data_by_setup(data, setup):
    '''
    获取前置条件的返回的数据
    :param data:
    :param setup:
    :return:
    '''
    if isinstance(data, dict):
        data = json.dumps(data)
    elif data == '':
        data = '{}'
    if setup:
        data = data.replace('\\', '')
        filed_all = re.findall(r'\"@(.*?)"', data)
        for filed in filed_all:
            try:
                rely_value = setup[filed]
                new_data = data.replace('@'+filed, rely_value)
            except Exception as e:
                logger('接口间数据传递').error(filed)
                logger('接口间数据传递').error(e)
            data = new_data
    return json.loads(data)
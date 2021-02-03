#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/26 13:43
# @Author  : kuangxiaojiang
# @File    : CompareData.py
# @Function: JSON比对
import json
import logging
from Utils.LoggerHandler import logger


def compare_data(json1, json2):
    '''
    数据对比
    :param json1: 数据1
    :param json2: 数据2
    :return:
    '''
    # 将str转dict
    if isinstance(json1, str):
        json1 = json.loads(json1)
    if isinstance(json2, str):
        json2 = json.loads(json2)

    if type(json1) == type(json2):
        if json1 == {} or json2 == {}:
            logger('【结果比对失败】').error('json1 或者 json2数据为空')
            raise AssertionError('json1 或者 json2数据为空')
        else:
            compare_data_sub(json1, json2)
    else:
        raise AssertionError('json1和json2数据类型不一致')


def compare_data_sub(data_a, data_b):
    '''
    数据比对
    :param data_a: 接口返回数据或自己设置的预期数据
    :param data_b: 数据库查询结果
    :return:
    '''
    if isinstance(data_a, dict):
        if len(data_a.keys()) == len(data_b.keys()):
            for key in data_a.keys():
                if isinstance(data_a[key], list) or isinstance(data_a[key], dict):
                    compare_data_sub(data_a[key], data_b[key])
                else:
                    try:
                        assert data_a[key] == data_b[key]
                    except Exception as e:
                        inf = "键值对%s  %s != %s" % (key, data_a[key], data_b[key])
                        logger('结果比对失败：').error(inf)
                        raise AssertionError(inf)
        else:
            inf = "data_1 键值对数量是%s != data2 键值对数量%s" % (len(data_a), len(data_b))
            logger('结果比对失败：').error("字典长度不相等")
            raise AssertionError(inf)

    elif isinstance(data_a, list):
        if len(data_a) != len(data_b):
            inf  = "data_1 长度是%s != data2 长度%s" % (len(data_a), len(data_b))
            logger('结果比对失败：').error("list 长度不相等")
            raise AssertionError(inf)
        else:
            for data_a_value, data_b_value in zip(data_a, data_b):
                if isinstance(data_a_value, list) or isinstance(data_a_value, dict):
                    compare_data_sub(data_a_value, data_b_value)
                else:
                    try:
                        assert data_a_value == data_b_value
                    except Exception as e:
                        inf = "列表%s中 %s != %s" % (data_a, data_a_value, data_b_value)
                        logger('结果比对失败：').error(inf)
                        raise AssertionError(inf)
    else:
        try:
            assert data_a == data_b
        except Exception as e:
            inf = " %s != %s" % (data_a, data_b)
            logger('结果比对失败：').error(inf)
            raise AssertionError(inf)

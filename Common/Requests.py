#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/24 12:41
# @Author  : kuangxiaojiang
# @File    : Requests.py
# @Function:
import requests
import json
from Utils.LoggerHandler import logger


class HttpRquests(object):
    def __int__(self):
        pass

    def send_post(self, url, data, headers=None):
        """
        发送POST请求
        :param url: url
        :param data: 请求数据
        :param headers: 请求头
        :return: 返回请求结果
        """

        # body = json.dumps(data, ensure_ascii=False).encode('UTF-8')
        body = data
        logger('body').debug(data)
        req = requests.Session()
        try:
            response_rst = req.post(url, json=body, headers=headers)
            rst = json.loads(response_rst.content)
            logger('rst: ').debug(rst)
        except Exception as e:
            logger().error('解析返回结果失败', e)
        if rst['code'] != 2000:
            logger().error('返回结果错误！状态码不为2000')
            logger().error(rst['message'])
            raise AssertionError(url, rst)
        else:
            return rst

    def send_get(self, url, data, headers=None):
        """
        发送GET请求
        :param url: url
        :param data: 请求数据
        :param headers: 请求头
        :return: 返回请求结果
        """
        logger('body').debug(data)
        req = requests.Session()
        try:
            response_rst = req.get(url, params=data, headers=headers)
            rst = json.loads(response_rst)
        except Exception as e:
            logger().error('解析返回结果失败', e)
        if rst['code'] != 2000:
            logger().error('返回结果错误！状态码不为2000')
            raise AssertionError(url, rst)
        else:
            return rst

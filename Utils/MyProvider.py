#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/10 9:28
# @Author  : kuangxiaojiang
# @File    : MyProvider.py
# @Function: 伪数据二次开发
from faker.providers import BaseProvider


class MyProvider(BaseProvider):
    '''
    根据公卫字典，二次封装faker库
    '''
    def test_1(self):
        return '测试数据信息'




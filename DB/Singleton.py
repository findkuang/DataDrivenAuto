#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/6 16:21
# @Author  : kuangxiaojiang
# @File    : Singleton.py
# @Function: 数据库对象单例模式

from functools import wraps


def singleton(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return get_instance
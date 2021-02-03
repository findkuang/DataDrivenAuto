#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/11 21:24
# @Author  : kuangxiaojiang
# @File    : RandomData.py
# @Function: 随机数生成器
from Utils.MyProvider import MyProvider
from faker import Faker
import re
import json


class RandomData(object):

    def __init__(self):
        self.interface_case_globals = {}
        self.interface_case_filed_list = []

    def get_random_data_value(self, data):
        if '%' in data:
            filed_key = re.findall(r'\"%(.*?)\"', data)[0]
            s_r = '%' + filed_key
            data_new = data.replace(s_r, self.interface_case_globals[filed_key])
            return data_new
        else:
            return data

    def random_data_format(self, data):
        '''
        根据随机函数，生成数据
        :param data: 格式化数据（类型为str）
        :return:
        '''
        faker = Faker(locale='zh_CN')
        faker.add_provider(MyProvider)
        if '\\"' in data:
            data_md = data.replace('\\', '')
            self.interface_case_filed_list = re.findall(r',\"(.{1,30}?)":\"faker.', data_md)
        else:
            data_md = data
            for key, value in json.loads(data_md).items():
                if 'faker.' in str(value):
                    self.interface_case_filed_list.append(key)

        rely_filed_list = re.findall(r'\"(faker.*?)\"', data_md)
        for i, rely_filed in enumerate(rely_filed_list):
            # 提取key待优化
            rely_filed = rely_filed.strip('\\')
            rely_value = str(eval(rely_filed))
            self.interface_case_globals[self.interface_case_filed_list[i]] = rely_value
            data_new = data.replace(rely_filed, rely_value)
            data = data_new
        return data
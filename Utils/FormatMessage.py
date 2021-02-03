#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/26 13:45
# @Author  : kuangxiaojiang
# @File    : FormatMessage.py
# @Function: 根据yml文件格式接口返回的报文
import yaml
import json
from Utils.LoggerHandler import logger


def format_data(original_data, target_yml):
    '''
    根据yml文件格式化json报文
    :param original_data: 原始报文数据
    :param target_yml: yml配置文件
    :return: 格式化后结果
    '''
    with open(target_yml, encoding='utf-8') as file:
        target_yml_data = yaml.full_load(file)
    rst_json = {}
    rst_json = get_sub_data_interface(original_data, target_yml_data, rst_json)
    return json.dumps(rst_json, ensure_ascii=False)


def get_sub_data_interface(original_data, target_yml_data, rst_data):
    '''
    格式化报文具体方法
    :param original_data: 原始数据
    :param target_yml_data: yml格式
    :param rst_data: 结果
    :return:
    '''
    if isinstance(original_data, list):
        for value in original_data:
            if isinstance(value, list):
                new_list = []
                new_rst = get_sub_data_interface(value, target_yml_data[0], new_list)
                rst_data.append(new_rst)
            elif isinstance(value, dict):
                new_json = {}
                new_rst = get_sub_data_interface(value, target_yml_data[0], new_json)
                rst_data.append(new_rst)
            else:
                rst_data.append(value)
    elif isinstance(original_data, dict):
        for key in target_yml_data.keys():
            if isinstance(original_data[key], dict):
                new_json = {}
                rst_data[key] = new_json
                get_sub_data_interface(original_data[key], target_yml_data[key], new_json)

            elif isinstance(original_data[key], list):
                new_list = []
                rst_data[key] = new_list
                for value in original_data[key]:
                    new_json = {}
                    new_rst = get_sub_data_interface(value, target_yml_data[key][0], new_json)
                    new_list.append(new_rst)
            else:
                rst_data[key] = original_data[key]
    return rst_data
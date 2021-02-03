#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/3 16:11
# @Author  : kuangxiaojiang
# @File    : FormatDbRst.py
# @Function: 根据yml文件格式化数据库查询的结果；
# 1.根据SQL文件中语句查询数据库，如果涉及到关联上一个查询结果，则需组装数据；如果非关联，则直接存储结果
# 2.根据yml字段，找出匹配的SQL结果，然后取出需要的值
# 3.逐层再次重复1-2的动作
# 查询结果之间的关系，独立非关联、依赖1-多或1-1、依赖多-多
from DB.MysqlHelper import MysqlHelper
import re
import yaml
import copy
import json
from Utils.LoggerHandler import logger


def get_db_format_data(sql_file, yml_file, **params):
    '''
    根据yml文件，将数据库查询结果格式化
    :param sql_file: sql文件
    :param yml_file: yml文件
    :return:
    '''
    with open(yml_file, encoding='utf-8') as file:
        target_yml_data = yaml.full_load(file)
    target_db_json = copy.deepcopy(target_yml_data)
    # 执行数据库查询
    query_rst_list, field_list_all = execute_sql_file(sql_file, **params)
    # 根据yml文件格式化数据库查询结果
    target_db_json = get_db_sub_format_data(query_rst_list, target_yml_data, field_list_all, target_db_json)
    return json.dumps(target_db_json, ensure_ascii=False)


def execute_sql_file(sql_file, **params):
    '''
    执行数据库查询
    :param sql_file:sql文件
    :return: 数据库查询结果， 数据库返回结果各字段
    '''
    with open(sql_file, encoding='utf-8') as f:
        sql_list = f.read().split(';')
        sql_list.pop()
        query_rst_list = []
        field_list_all = []
        for sql in sql_list:
            # 获取sql中各查询字段
            sql = sql.replace('from', 'FROM').replace('as', 'AS')
            field_str = sql.split('FROM')[0].replace('\n', '')+','
            field_list = re.findall('AS (.+?),', field_str)
            # 参数化sql
            param_fields = re.findall('\'{(.+?)}\'', sql)
            if not set(param_fields).issubset(list(params['query'].keys())):
                # 如果查询条件字段没在excel中,而是依赖其他SQL语句执行结果,则该语句查询结果与其他SQL结果相关联
                param_other_list = [param for param in param_fields if param not in params['query'].keys()]
                param_related = param_other_list[0]
                # 如果该查询结果与其他查询关联，则field_list为空
                field_list = []
                for query_rst in query_rst_list:
                    # 需要做递归嵌套数据处理，获取查询结果中每个层级的keys和层级深度：
                    layerKeysData = {}
                    layer = 0
                    layerKeysData = get_keys_layer_from_data(query_rst, layerKeysData, layer)
                    for deep, keys in layerKeysData.items():
                        if set(param_other_list).issubset(keys):
                            # 根据层级深度组装数据,将数据库关联的数据组装成树形结构
                            combination_data(query_rst, int(deep), param_related, sql, **params)
            else:
                query_rst = connect_db_and_execute(sql, **params)
                # 获取数据库查询结果
                query_rst_list.append(query_rst)
            # 获取每个sql里面的字段名称
            field_list_all.append(field_list)
    return query_rst_list, field_list_all


def combination_data(query_rst, deep, param_related, sql, **params):
    '''
    将数据库查询结果组装成树形结构
    :param query_rst: 查询结果
    :param deep: 层级
    :param param_related: sql语句中需要关联的字段
    :param sql: sql语句
    :param params: 查询参数
    :return:
    '''
    if deep == 1:
        for index, db_rst in enumerate(query_rst):
            params['query'][param_related] = query_rst[index][param_related]
            # 将关联的查询结果与主查询结果数据合并为一组
            related_query_rst = connect_db_and_execute(sql, **params)
            query_rst[index][param_related] = related_query_rst
    else:
        deep = deep - 1
        for index, db_rst in enumerate(query_rst):
            sub_data = [value for value in db_rst.values() if isinstance(value, list)]
            if sub_data:
                combination_data(sub_data[0], deep, param_related, sql, **params)
    return query_rst


def get_keys_layer_from_data(data, layerKeysData, layer):
    '''
    获取数据中的每一层级中的keys，一个字典嵌套为一层
    :param data: 数据
    :param layerKeysData: 层级：keys数据
    :param layer: 层级
    :return:
    '''
    keys_data = []
    if isinstance(data, dict):
        layer = layer + 1
        layerKeysData[str(layer)] = keys_data + (list(data.keys()))
        for key, value in data.items():
            if isinstance(value, dict):
                get_keys_layer_from_data(value, layerKeysData, layer)
            elif isinstance(value, list):
                get_keys_layer_from_data(value, layerKeysData, layer)

    elif isinstance(data, list):
        if isinstance(data[0], dict):
            get_keys_layer_from_data(data[0], layerKeysData, layer)
    return layerKeysData


def connect_db_and_execute(sql, **params):
    '''
    连接数据库，并执行SQL语句
    :param sql: SQL语句
    :param params: 执行参数
    :return:
    '''
    sql = sql.format(**params['query'])
    logger('【执行SQL语句】').debug(sql)
    # 获取数据库db信息
    db_name = (re.findall('(.+?)\.', sql.split('FROM')[1])[0]).replace('\t', '').strip()
    # 连接数据库并查询
    db = MysqlHelper('mysql-test', db_name)
    query_rst = db.get_all(sql)
    return query_rst


def get_db_sub_format_data(query_rst_list, target_yml_data, field_list_all, target_db_json):
    '''
    根据yml文件格式化数据库查询结果
    :param query_rst_list: 数据库查询结果列表
    :param target_yml_data: yml格式化数据
    :param field_list_all: 字段列表
    :param target_db_json: 格式化后的结果
    :return:
    '''
    if isinstance(target_yml_data, dict):
        for key in target_yml_data.keys():
            if isinstance(target_yml_data[key], dict):
                get_db_sub_format_data(query_rst_list, target_yml_data[key], field_list_all, target_db_json[key])
            elif isinstance(target_yml_data[key], list):
                for index, field_list in enumerate(field_list_all):
                    if list(target_yml_data[key][0].keys())[0] in field_list:
                        rst = get_db_sub_format_data(query_rst_list, target_yml_data[key], field_list_all, target_db_json[key])
                        target_db_json[key] = rst
            else:
                if isinstance(target_db_json, dict):
                    for index, field_list in enumerate(field_list_all):
                        if key in field_list:
                            if len(query_rst_list[index]) == 1:
                                target_db_json[key] = query_rst_list[index][0][key]
                else:
                    for index, field_list in enumerate(field_list_all):
                        if list(target_yml_data.keys())[0] in field_list and index <= len(query_rst_list)-1:
                            for i in range(len(query_rst_list[index])):
                                new_json = copy.deepcopy(target_yml_data)
                                for key in target_yml_data.keys():
                                    if key in list(query_rst_list[index][i].keys()):
                                        new_json[key] = query_rst_list[index][i][key]
                                    else:
                                        new_json[key] = ""
                                target_db_json.append(new_json)
                    target_db_json.pop(0)
                    break
    elif isinstance(target_yml_data, list):
        for value in target_yml_data:
            if isinstance(value, dict):
                get_db_sub_format_data(query_rst_list, target_yml_data[0], field_list_all, target_db_json)
            elif isinstance(value, list):
                get_db_sub_format_data(query_rst_list, target_yml_data[0], field_list_all, target_db_json)
    return target_db_json






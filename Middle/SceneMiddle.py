#!/usr/bin/env python
# @Time    : 2020/9/18 23:02
# @Author  : kuangxiaojiang
# @File    : SceneMiddle.py
# @Function: 场景类用例中间层
'''
步骤：
1.场景接口地址列表配置
2.各接口参数配置
3.接口依赖传值
4.最终场景结束后，结果验证
'''
from Common.Login import Login
from Utils.FormatMessage import format_data
from Utils.CompareData import compare_data
from Utils.FormatDbRst import get_db_format_data
from Utils.GetConfigInfo import URL_INFO
import jsonpath
import re
import json
from Utils.LoggerHandler import logger
from Utils.FormatOtherData import format_body_by_rely
from Utils.FormatOtherData import format_data_by_setup
from DB.DbAPI import query_db


def scene_middle_verify(username, pwd, scene_data, setUp=None):
    '''
    场景类自动化用例验证
    :param username: 登录用户名
    :param pwd: 登陆密码
    :param scene_data: 场景类的驱动数据
    :param setUp: 前置条件返回的结果数据
    :return:
    '''
    # 登录
    # lg = Login(username, pwd)
    # access_token, req = lg.login()
    # defaultLoc, defaultIns = lg.get_default_setting(req, access_token)
    # headers = {"Authorization": 'Bearer '+ access_token,
    #            "k2": defaultLoc,
    #            "k1": defaultIns,
    #            "Content-Type": "application/json; charset=UTF-8"
    # }
    lg = Login(username, pwd)
    req = lg.req
    headers = {"Authorization": 'Bearer '+ lg.access_token,
               "k2": lg.defaultLoc,
               "k1": lg.defaultIns
    }
    # 将接口依赖关系存存入dict
    interface_relations = {}
    for interface_data in scene_data:
        interface_relations[interface_data['uri']] = interface_data['rely']

    # 解析接口依赖关系,梳理接口依赖关系；决定接口执行顺序，(场景接口数据根据接口依赖重新排序)
    scene_data_new = []
    for interface, rely_interface in interface_relations.items():
        for scene in scene_data:
            if rely_interface == "" and rely_interface == scene['rely']:
                scene_data_new.append(scene)
    for scene_new in scene_data_new:
        for scene in scene_data:
            if scene['rely'] == scene_new['uri']:
                scene_data_new.append(scene)

    # 然后针对每个接口发送请求，根据接口依赖取值，并保存；提供给其他依赖与此接口的返回值；
    # 接口返回结果
    reponse_rst_dict = {}
    for index, interface_data in enumerate(scene_data_new):
        # 发送接口请求
        uri = interface_data['uri']
        # 根据场景的前置条件格式化body
        body = format_data_by_setup(interface_data['body'], setUp)

        if interface_data['rely']:
            # 获取依赖的数据，并格式化body,将依赖的数据写入填充到body里面
            body = format_body_by_rely(interface_data['body'], reponse_rst_dict[interface_data['rely']])
        # 打印body日志
        logger('请求报文body为：').debug(body)
        if isinstance(body, str):
            body = json.loads(body)
        url = URL_INFO['TEST']['url'] + uri
        if interface_data['send_method'] == 'POST':
            rst = req.send_post(url, data=body, headers=headers)
        else:
            rst = req.send_get(url, data=body, headers=headers)
        # 如果SQL执行字段为空，则保存接口返回结果; 否则查询数据库结果保存
        if interface_data['sql'] and index < len(scene_data_new)-1:
            sql_file = interface_data['sql']
            condition = json.loads(interface_data['condition'])
            db_rst = query_db(sql_file, query=condition)
            reponse_rst_dict[uri] = db_rst[0]
        else:
            if rst:
                reponse_rst_dict[uri] = rst
            else:
                logger(uri).error('接口返回结果错误！')
                raise AssertionError(uri, '接口返回结果错误')
    # 最后一个接口结束后，验证场景结果
    # 如果最后一个接口是查询类，则写SQL查询校验
    if scene_data_new[-1]['interface_type'] == 0:
        rst = reponse_rst_dict[scene_data_new[-1]['uri']]
        yml_file = scene_data_new[-1]['yml']
        sql_file = scene_data_new[-1]['sql']
        expected_rst = scene_data_new[-1]['expected_rst']
        # condition = json.loads(scene_data_new[-1]['condition'])
        condition = json.loads(format_body_by_rely(scene_data_new[-1]['condition'], reponse_rst_dict[interface_data['rely']]))
        target_json = format_data(rst, yml_file)
        logger('接口返回结果根据YML格式化为：').debug(target_json)
        # 如果expected_rst 期望结果不为空，则直接expected_rst与target_json比对；
        if expected_rst:
            compare_data(target_json, expected_rst)
        else:
            # 查询数据库，执行数据库查询并返回格式化后的结果
            fm_db_rst = get_db_format_data(sql_file, yml_file, query=condition)
            logger('数据库查询结果根据YML格式化为：').debug(fm_db_rst)
            # 数据库查询结果和接口返回结果比对
            logger('【=====接口需比对数据：=====】').debug(target_json)
            logger('【=====数据库需比对数据：=====】').debug(fm_db_rst)
            compare_data(target_json, fm_db_rst)
    # 如果最后一个接口是提交类，则直接执行SQL查询结果
    else:
        # 数据库查询校验
        expected_rst = scene_data_new[-1]['expected_rst']
        yml_file = scene_data_new[-1]['yml']
        sql_file = scene_data_new[-1]['sql']
        # condition = json.loads(scene_data_new[-1]['condition'])
        condition = json.loads(format_body_by_rely(scene_data_new[-1]['condition'], reponse_rst_dict[interface_data['rely']]))
        if yml_file == '':
            db_rst = query_db(sql_file, query=condition)
            logger('数据库查询结果：').debug(db_rst)
            if len(db_rst) > 0:
                fm_db_rst = json.dumps(db_rst[0])
            else:
                logger('数据库查询结果：').error('数据库查询结果为空')
                fm_db_rst = '{}'

        else:
            fm_db_rst = get_db_format_data(sql_file, yml_file, query=condition)
            logger('数据库查询结果根据YML格式化为：').debug(fm_db_rst)
        # 数据库查询结果和预期结果比对
        logger('【=====expected_rst预期结果为：=====】').debug(expected_rst)
        logger('【=====数据库需比对数据：=====】').debug(fm_db_rst)
        compare_data(expected_rst, fm_db_rst)
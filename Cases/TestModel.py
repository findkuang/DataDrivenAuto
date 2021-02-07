#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/28 18:00
# @Author  : Aisonk
# @File    : TestModel.py
# @Function:
import pytest
from Middle.QueryMiddle import get_query_compare_rst
from Middle.SubmitMiddle import submit_data_and_verify
from Middle.SceneMiddle import scene_middle_verify
import allure
from Utils.GetConfigInfo import USER_INFO
from Utils.GetConfigInfo import EXCEL_PATH_INFO
from DataDriven.ExcelInterfaceHandle import get_excel_interface_data
from DataDriven.ExcelSenceHandle import get_excel_scene_data

# 获取所有excel文件的用例数据
test_data_list = []
for file_path in EXCEL_PATH_INFO:
    if '接口_' in file_path:
        interface_list_qr, interface_list_sm = get_excel_interface_data(file_path.replace('\n', ''))
        test_data_list.extend(interface_list_qr)
        test_data_list.extend(interface_list_sm)
    elif '场景_' in file_path:
        file_path = file_path.replace('\n', '')
        scene_data = get_excel_scene_data(file_path)
        test_data_list.extend(scene_data)


@pytest.mark.usefixtures('case')
@pytest.mark.parametrize('case', test_data_list, indirect=True)
def test_interface_query(case):
    '''
    接口-查询类型用例数据驱动模板
    :param case: 查询类型用例数据
    :return:
    '''
    # 如果用例为接口类型
    if isinstance(case, dict):
        uri = case['uri']
        body = case['body']
        conditions = case['conditions']
        send_method = case['send_method']
        sql_path = case['sql_path']
        yml_path = case['yml_path']
        expected_rst = case['expected_rst']
        setUp = case['setUp']
        # 制作测试报告
        allure.dynamic.feature(case['module'])
        allure.dynamic.story(case['sub_module'])
        allure.dynamic.title(case['case_name'])
        if case['interface_type'] == '0':
            # 调用单接口查询类型
            get_query_compare_rst(USER_INFO['xtest01']['username'], USER_INFO['xtest01']['password'], uri, body,
                                  expected_rst, sql_path, yml_path, send_method, setUp=setUp, query=conditions)
        elif case['interface_type'] == '1':
            # 调用单接口提交类ing
            submit_data_and_verify(USER_INFO['xtest01']['username'], USER_INFO['xtest01']['password'], uri, body,
                                   expected_rst,
                                   sql_path, yml_path, send_method, setUp=setUp, query=conditions)
    # 如果用例为场景类型
    elif isinstance(case, list):
        setUp = case[0]['setUp']
        # 制作测试报告
        allure.dynamic.feature(case[0]['module'])
        allure.dynamic.story(case[0]['sub_module'])
        allure.dynamic.title(case[0]['scene_name'])
        scene_middle_verify(USER_INFO['vivi']['username'], USER_INFO['vivi']['password'], case, setUp=setUp)
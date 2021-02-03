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
interface_list_queryType = []
interface_list_submitType = []
scene_data_list = []
for file_path in EXCEL_PATH_INFO:
    if '接口' in file_path:
        interface_list_qr, interface_list_sm = get_excel_interface_data(file_path.replace('\n', ''))
        interface_list_queryType.extend(interface_list_qr)
        interface_list_submitType.extend(interface_list_sm)
    # elif '场景' in file_path:
    #     file_path = file_path.replace('\n', '')
    #     scene_data = get_excel_scene_data(file_path)
    #     scene_data_list.extend(scene_data)

@pytest.mark.usefixtures('')
@pytest.mark.parametrize('case', interface_list_queryType)
def test_interface_query(case):
    '''
    接口-查询类型用例数据驱动模板
    :param case: 查询类型用例数据
    :return:
    '''
    uri = case['uri']
    body = case['body']
    conditions = case['conditions']
    send_method = case['send_method']
    sql_path = case['sql_path']
    yml_path = case['yml_path']
    expected_rst = case['expected_rst']
    # 制作测试报告
    allure.dynamic.feature(case['module'])
    allure.dynamic.story(case['sub_module'])
    allure.dynamic.title(case['case_name'])

    # 调用单接口查询类型
    get_query_compare_rst(USER_INFO['xtest01']['username'], USER_INFO['xtest01']['password'], uri, body,
                          expected_rst, sql_path, yml_path, send_method, setUp=None, query=conditions)


@pytest.mark.parametrize('case', interface_list_submitType)
def test_interface_submit(case):
    '''
    接口-提交类型用例数据驱动模板
    :param case:
    :return:
    '''
    uri = case['uri']
    body = case['body']
    conditions = case['conditions']
    send_method = case['send_method']
    sql_path = case['sql_path']
    yml_path = case['yml_path']
    expected_rst = case['expected_rst']
    # 制作测试报告
    allure.dynamic.feature(case['module'])
    allure.dynamic.story(case['sub_module'])
    allure.dynamic.title(case['case_name'])
    #调用提交类型接口
    submit_data_and_verify(USER_INFO['xtest01']['username'], USER_INFO['xtest01']['password'], uri, body, expected_rst,
                           sql_path, yml_path, send_method, setUp=None, query=conditions)


# @pytest.mark.parametrize('scene', scene_data_list)
# def test_interface_submit(scene):
#     '''
#     场景-用例类型数据驱动模板
#     :param scene: 场景数据
#     :return:
#     '''
#     # 制作测试报告
#     allure.dynamic.feature(scene[0]['module'])
#     allure.dynamic.story(scene[0]['sub_module'])
#     allure.dynamic.title(scene[0]['case_name'])
#     scene_middle_verify(USER_INFO['vivi']['username'], USER_INFO['vivi']['password'], scene, setUp=add_user_base_info)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/28 13:42
# @Author  : Aisonk
# @File    : ExcelInterfaceHandle.py
# @Function: 接口用例数据驱动
import json
import os
import xlrd
from Utils.RandomData import RandomData


def get_excel_interface_data(file_path):
    '''
    获取接口的查询类型和提交类型的所有用例
    :param file_path:
    :return:
    '''
    book = xlrd.open_workbook(file_path)
    interface_list_queryType = []
    interface_list_submitType = []
    # 拿到表格中对象 按索引获取
    sheet = book.sheet_by_index(0)
    for row in range(1, sheet.nrows):
        if int(sheet.cell(row, 3).value) == 0:
            # 获取接口中的信息
            interface = {}
            random_obj = RandomData()
            interface['module'] = sheet.cell(row, 0).value
            interface['sub_module'] = sheet.cell(row, 1).value
            interface['case_name'] = sheet.cell(row, 2).value
            interface['interface_type'] = str(int(sheet.cell(row, 3).value))
            interface['uri'] = sheet.cell(row, 4).value
            interface['send_method'] = sheet.cell(row, 5).value
            interface['body'] = json.loads(random_obj.random_data_format(sheet.cell(row, 6).value))
            interface['sql_path'] = sheet.cell(row, 7).value
            interface['conditions'] = json.loads(random_obj.get_random_data_value(sheet.cell(row, 8).value))
            interface['yml_path'] = sheet.cell(row, 9).value
            interface['expected_rst'] = random_obj.get_random_data_value(sheet.cell(row, 10).value)
            interface['setUp'] = sheet.cell(row, 11).value
            interface_list_queryType.append(interface)
        elif int(sheet.cell(row, 3).value) == 1:
            interface = {}
            random_obj = RandomData()
            interface['module'] = sheet.cell(row, 0).value
            interface['sub_module'] = sheet.cell(row, 1).value
            interface['case_name'] = sheet.cell(row, 2).value
            interface['interface_type'] = str(int(sheet.cell(row, 3).value))
            interface['uri'] = sheet.cell(row, 4).value
            interface['send_method'] = sheet.cell(row, 5).value
            interface['body'] = json.loads(random_obj.random_data_format(sheet.cell(row, 6).value))
            interface['sql_path'] = sheet.cell(row, 7).value
            interface['conditions'] = json.loads(random_obj.get_random_data_value(sheet.cell(row, 8).value))
            interface['yml_path'] = sheet.cell(row, 9).value
            interface['expected_rst'] = random_obj.get_random_data_value(sheet.cell(row, 10).value)
            interface['setUp'] = sheet.cell(row, 11).value
            interface_list_submitType.append(interface)
    return interface_list_queryType, interface_list_submitType


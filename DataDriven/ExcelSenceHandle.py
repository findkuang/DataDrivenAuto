#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/28 13:44
# @Author  : Aisonk
# @File    : ExcelSenceHandle.py
# @Function: 接口用例数据驱动
import xlrd
from Utils.RandomData import RandomData

scene_all = {}


def get_excel_scene_data(file_path):
    '''
    获取场景类型的执行用例
    :param file_path:
    :return:
    '''
    book = xlrd.open_workbook(file_path)

    # 拿到表格中对象 按索引获取
    sheet = book.sheet_by_index(0)
    file_obj = 0
    # 获取所有场景数据
    scene_dict = {}
    for row in range(1, sheet.nrows):
        scene_name = sheet.cell(row, 2).value

        if scene_name not in scene_all.keys():
            scene = []
            if not scene:
                random_obj = RandomData()
                interface_dict = {}
                # 获取接口中的信息
                interface_dict['module'] = sheet.cell(row, 0).value
                interface_dict['sub_module'] = sheet.cell(row, 1).value
                interface_dict['scene_name'] = sheet.cell(row, 2).value
                interface_dict['interface_name'] = sheet.cell(row, 3).value
                interface_dict['interface_type'] = sheet.cell(row, 4).value
                interface_dict['uri'] = sheet.cell(row, 5).value
                interface_dict['send_method'] = sheet.cell(row, 6).value
                interface_dict['body'] = random_obj.random_data_format(sheet.cell(row, 7).value)
                interface_dict['rely'] = sheet.cell(row, 8).value
                interface_dict['sql'] = sheet.cell(row, 9).value
                interface_dict['condition'] = random_obj.get_random_data_value(sheet.cell(row, 10).value)
                interface_dict['yml'] = sheet.cell(row, 11).value
                interface_dict['expected_rst'] = random_obj.get_random_data_value(sheet.cell(row, 12).value)
                interface_dict['setUp'] = sheet.cell(row, 13).value
                scene.append(interface_dict)
                scene_dict[scene_name] = scene
                scene_all[scene_name] = scene
        else:
            random_obj = RandomData()
            interface_dict = {}
            # 获取接口中的信息
            interface_dict['module'] = sheet.cell(row, 0).value
            interface_dict['sub_module'] = sheet.cell(row, 1).value
            interface_dict['scene_name'] = sheet.cell(row, 2).value
            interface_dict['interface_name'] = sheet.cell(row, 3).value
            interface_dict['interface_type'] = sheet.cell(row, 4).value
            interface_dict['uri'] = sheet.cell(row, 5).value
            interface_dict['send_method'] = sheet.cell(row, 6).value
            interface_dict['body'] = random_obj.random_data_format(sheet.cell(row, 7).value)
            interface_dict['rely'] = sheet.cell(row, 8).value
            interface_dict['sql'] = sheet.cell(row, 9).value
            interface_dict['condition'] = sheet.cell(row, 10).value
            interface_dict['yml'] = sheet.cell(row, 11).value
            interface_dict['expected_rst'] = sheet.cell(row, 12).value
            interface_dict['setUp'] = sheet.cell(row, 13).value
            scene_dict[scene_name] = scene
            scene_all[scene_name].append(interface_dict)
    # 根据场景生成自动化测试脚本
    return scene_all.values()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/19 19:12
# @Author  : kuangxiaojiang
# @File    : ExcelSenceOpt.py
# @Function: 场景类接口案例自动生成
import xlrd
import json
import os
import pinyin
from Utils.RandomData import RandomData

Cases_dir = os.getcwd() + '\\Cases' + '\\Scene'
scene_all = {}


def excel_scene_opt(file_path):
    '''
    场景类型测试用例自动化生成
    :param file_path: excel数据驱动文件路径
    :return: 自动生成的场景测试用例文件
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
    return scene_dict


def scene_entrance(file_path):
    file_list = []
    scene_dict = excel_scene_opt(file_path)
    file_obj = 0
    for scene_name, scene in scene_dict.items():

        module_eg, sub_module_eg, scene_name_eg = chinese_convert_pingyin(scene[0]['module'], scene[0]['sub_module'], scene[0]['scene_name'])
        if not os.path.isdir(Cases_dir + '\\' + module_eg):
            os.makedirs(Cases_dir + '\\' + module_eg)
        if not os.path.isfile(Cases_dir + '\\' + module_eg + '\\' + sub_module_eg + '.py'):
            file_obj = create_import_scripts(Cases_dir, scene[0]['module'], scene[0]['sub_module'], module_eg, sub_module_eg, scene_name, scene[0]['setUp'])
        else:
            if not file_obj:
                # 清空文件内容，再重新写入自动化测试案例
                with open(Cases_dir + '\\' + module_eg + '\\' + sub_module_eg + '.py', 'r+') as file:
                    file.truncate(0)
                # 打开文件，重新写入import scripts
                file_obj = create_import_scripts(Cases_dir, scene[0]['module'], scene[0]['sub_module'], module_eg, sub_module_eg, scene_name, scene[0]['setUp'])
            else:
                create_auto_scene_cases(scene[0]['module'], scene[0]['sub_module'], scene[0]['scene_name'], scene[0]['setUp'], file_obj)
    file_obj.close()
    file_list.append(file_obj.name)
    return file_list


def create_import_scripts(Cases_dir, module, sub_module, module_eg, sub_module_eg, scene_name, setup):
    sub_module_file = open(Cases_dir + '\\' + module_eg + '\\' + sub_module_eg + '.py', mode="w",
                           encoding="utf-8")
    import_script = '''
import pytest
import os
import allure
from Utils.GetConfigInfo import USER_INFO
from Middle.SceneMiddle import scene_middle_verify
from DataDriven.ExcelSenceOpt import scene_all
                            '''
    sub_module_file.write(import_script)
    create_auto_scene_cases(module, sub_module, scene_name, setup, sub_module_file)
    return sub_module_file


def create_auto_scene_cases(module, sub_module, scene_name, setup, file_obj):
    module_eg, sub_module_eg, scene_name_eg = chinese_convert_pingyin(module, sub_module, scene_name)
    if not setup:
        # 前置条件
        function_setup = None
    else:
        function_setup = setup
    test_script = '''

@allure.feature('{}')
@allure.story('{}')
@allure.title('{}')
def test_scene_{}({}):
    scene_data = scene_all['{}']
    scene_middle_verify(USER_INFO['vivi']['username'], USER_INFO['vivi']['password'], scene_data, setUp={})
        '''.format(module, sub_module, scene_name, scene_name_eg, setup, scene_name, function_setup)
    file_obj.write(test_script)


def chinese_convert_pingyin(module, sub_module, scene_name):
    '''
    将中文转换成拼音
    :param module:
    :param sub_module:
    :param case_name:
    :return:
    '''
    module = pinyin.get(module, format="strip", delimiter="")
    sub_module = 'Test_' + pinyin.get(sub_module, format="strip", delimiter="")
    scene_name = pinyin.get(scene_name, format="strip", delimiter="")
    return module, sub_module, scene_name

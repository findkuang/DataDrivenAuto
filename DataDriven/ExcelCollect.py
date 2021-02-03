#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/4 23:08
# @Author  : kuangxiaojiang
# @File    : ExcelCollect.py
# @Function: Excel 测试用例文件收集
from DataDriven.ExcelInterfaceOpt import interface_entrance
from DataDriven.ExcelSenceOpt import scene_entrance
import os
AutoTestFiles_path = r'D:\AutoTestFiles'


def excel_collect(file_path=None):
    '''
    excel 测试用例文件收集
    :param file_path: excel路径
    :return: 返回测试用例Py文件列表
    '''
    file_list = []
    if file_path:
        dir_name, file_name = os.path.split(file_path)
        if file_name.startswith('接口_'):
            file_list = interface_entrance(file_path)
        elif file_name.startswith('场景_'):
            file_list = scene_entrance(file_path)
    else:
        # 遍历目录下所有excel文件，然后遍历解析excel测试用例
        for root, dirs, files in os.walk(AutoTestFiles_path):
            for file in files:
                if file.endswith('xlsx') and file.startswith('场景_'):
                    file_path = os.path.join(root, file)
                    file_scene_list = scene_entrance(file_path)
                    file_list.extend(file_scene_list)
                elif file.endswith('xlsx') and file.startswith('接口_'):
                    file_path = os.path.join(root, file)
                    file_inf_list = interface_entrance(file_path)
                    file_list.extend(file_inf_list)
    return file_list
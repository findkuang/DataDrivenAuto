#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/28 19:45
# @Author  : Aisonk
# @File    : ExcelHandle.py
# @Function:
import os
current_dir = os.getcwd()
AutoTestFiles_path = r'D:\AutoTestFiles'


def set_file_path_config(path=None):
    '''
    设置要执行的配置文件路径
    :param path:
    :return:
    '''
    # 修改file_path配置文件数据
    file_config_dir = current_dir + "\\Config\\File_path_list.txt"
    with open(file_config_dir, 'w', encoding='utf-8') as file_obj:
        file_obj.truncate(0)
        if path:
            # 如果传递的路径有值，则写入到文件配置
            file_obj.write(path+'\n')
        else:
            # 如果没有传递路径，则默认执行所有的用例文件
            for root, dirs, files in os.walk(AutoTestFiles_path):
                if files:
                    for file in files:
                        if file.endswith('.xlsx'):
                            file_path = os.path.join(root, file)
                            file_obj.write(file_path+'\n')




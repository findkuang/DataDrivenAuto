#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/3 23:41
# @Author  : kuangxiaojiang
# @File    :
# @Function: 自动化测试框架运行入口
import pytest
import os
from DataDriven.ExcelHandle import set_file_path_config


if __name__ == '__main__':
    # # 执行命令 allure generate ./temp -o ./report --clean ，生成测试报告
    # os.system('allure generate ./Temp -o ./Report --clean-alluredir')
    # os.system('pytest .\Cases\danganguanli\Test_gerendangan.py --alluredir C:\Windows\System32\config\systemprofile\AppData\Local\Jenkins\.jenkins\workspace\自动化测试Job\\allure-results --clean-alluredir')

    # # 需要执行文件路径
    file_path = r'D:\AutoTestFiles\接口\接口_健康档案模块.xlsx'
    set_file_path_config(file_path)
    pytest.main([])
    os.system('allure serve ./Temp  ./Report')





#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/19 19:11
# @Author  : kuangxiaojiang
# @File    : ExcelInterfaceOpt.py
# @Function: 自动生成单接口类型的测试用例
import xlrd
import pytest
import os
import allure
from Utils.GetConfigInfo import USER_INFO
import json
import os
import pinyin
from Utils.RandomData import RandomData


Cases_dir = os.getcwd() + '\\Cases' + '\\Interface'


def interface_entrance(file_path):
    '''
    自动生成单接口自动化用例入口
    :param file_path: excel数据驱动文件路径
    :return: 自动生成的单接口测试用例文件
    '''
    file_list = []
    file_obj = 0
    sub_module_flag = ''
    # 获取excel中接口列表信息
    interface_list = get_excel_interface_info(file_path)
    for interface in interface_list:
        # 生成模块文件夹
        module_name_eg, sub_module_eg, case_name_eg = chinese_convert_pingyin(interface['module'], interface['sub_module'], interface['case_name'])
        if not os.path.isdir(Cases_dir + '\\' + module_name_eg):
            os.makedirs(Cases_dir + '\\' + module_name_eg)
        if not os.path.isfile(Cases_dir + '\\' + module_name_eg + '\\' + sub_module_eg + '.py'):
            file_obj = create_import_scripts(Cases_dir, module_name_eg, sub_module_eg, interface['module'], interface['sub_module'],
                        interface['case_name'], interface['interface_type'], interface['uri'], interface['send_method'], interface['body'],
                        interface['sql_path'], interface['conditions'], interface['yml_path'], interface['expect_rst'],interface['setUp'])
        else:
            # 如果首次进入文件
            if not file_obj:
                # 清空文件内容，再重新写入自动化测试案例
                with open(Cases_dir + '\\' + module_name_eg + '\\' + sub_module_eg + '.py', 'r+') as file:
                    file.truncate(0)
                # 打开文件，重新写入import scripts
                file_obj = create_import_scripts(Cases_dir, module_name_eg, sub_module_eg, interface['module'], interface['sub_module'],
                        interface['case_name'], interface['interface_type'], interface['uri'], interface['send_method'], interface['body'],
                        interface['sql_path'], interface['conditions'], interface['yml_path'], interface['expect_rst'], interface['setUp'])
                sub_module_flag = sub_module_eg
            elif file_obj and sub_module_eg != sub_module_flag:
                # 关闭上一个子模块自动化py测试文件
                file_obj.close()
                file_list.append(file_obj.name)
                # 清空文件内容，再重新写入自动化测试案例
                with open(Cases_dir + '\\' + module_name_eg + '\\' + sub_module_eg + '.py', 'r+') as file:
                    file.truncate(0)
                # 打开文件，重新写入import scripts
                file_obj = create_import_scripts(Cases_dir, module_name_eg, sub_module_eg, interface['module'], interface['sub_module'],
                        interface['case_name'], interface['interface_type'], interface['uri'], interface['send_method'], interface['body'],
                        interface['sql_path'], interface['conditions'], interface['yml_path'], interface['expect_rst'], interface['setUp'])
                sub_module_flag = sub_module_eg
            else:
                create_auto_cases(interface['module'], interface['sub_module'], interface['case_name'], interface['interface_type'],
                                  interface['uri'], interface['send_method'], interface['body'], interface['sql_path'],
                                  interface['conditions'], interface['yml_path'], interface['expect_rst'], interface['setUp'], file_obj)
                sub_module_flag = sub_module_eg
    file_obj.close()
    file_list.append(file_obj.name)
    return file_list


def get_excel_interface_info(file_path):
    book = xlrd.open_workbook(file_path)
    interface_list = []
    # 拿到表格中对象 按索引获取
    sheet = book.sheet_by_index(0)
    for row in range(1, sheet.nrows):
        # 获取接口中的信息
        interface = {}
        random_obj = RandomData()
        interface['module'] = sheet.cell(row, 0).value
        interface['sub_module'] = sheet.cell(row, 1).value
        interface['case_name'] = sheet.cell(row, 2).value
        interface['interface_type'] = sheet.cell(row, 3).value
        interface['uri'] = sheet.cell(row, 4).value
        interface['send_method'] = sheet.cell(row, 5).value
        interface['body'] = json.loads(random_obj.random_data_format(sheet.cell(row, 6).value))
        interface['sql_path'] = sheet.cell(row, 7).value
        interface['conditions'] = json.loads(random_obj.get_random_data_value(sheet.cell(row, 8).value))
        interface['yml_path'] = sheet.cell(row, 9).value
        interface['expect_rst'] = random_obj.get_random_data_value(sheet.cell(row, 10).value)
        interface['setUp'] = sheet.cell(row, 11).value
        interface_list.append(interface)
    return interface_list


def create_import_scripts(Cases_dir,module_name_eg,sub_module_eg,module, sub_module, case_name,
                          interface_type, uri, send_method, body,sql_path, conditions, yml_path,
                          expect_rst, setUp):
    sub_module_file = open(Cases_dir + '\\' + module_name_eg + '\\' + sub_module_eg + '.py', mode="w",
                           encoding="utf-8")
    import_script = '''
import pytest
import os
from Middle.QueryMiddle import get_query_compare_rst
from Middle.SubmitMiddle import submit_data_and_verify
import allure
from Utils.GetConfigInfo import USER_INFO
                        '''
    sub_module_file.write(import_script)
    create_auto_cases(module, sub_module, case_name, interface_type, uri, send_method, body,
                      sql_path, conditions, yml_path, expect_rst, setUp, sub_module_file)
    return sub_module_file


def create_auto_cases(module,sub_module,case_name,interface_type,uri,send_method,body,
                      sql_path,conditions,yml_path,expect_rst,setUp,sub_module_file):
    # 生成模块文件夹
    module_name_eg, sub_module_eg, case_name_eg = chinese_convert_pingyin(module, sub_module, case_name)
    if not setUp:
        # 前置条件
        function_setup = None
    else:
        function_setup = setUp
    # 接口类型为查询类型
    if interface_type == 0:
        test_script = '''
        
@allure.feature('{}')
@allure.story('{}')
@allure.title('{}')
def test_interface_{}({}):
    uri = '{}'
    body = {}
    conditions = {}
    send_method = '{}'
    sql_path = r'{}'
    yml_path = r'{}'
    expected_rst = '{}'
    get_query_compare_rst(USER_INFO['xtest01']['username'], USER_INFO['xtest01']['password'], uri, body, expected_rst, sql_path, yml_path, send_method,setUp={},query=conditions)
        '''.format(module, sub_module, case_name, case_name_eg, setUp, uri, body, conditions,send_method, sql_path, yml_path, expect_rst,function_setup)
    else:
        test_script = '''

@allure.feature('{}')
@allure.story('{}')
@allure.title('{}')
def test_interface_{}({}):
    uri = '{}'
    body = {}
    conditions = {}
    send_method = '{}'
    sql_path = r'{}'
    yml_path = r'{}'
    expected_rst = '{}'
    submit_data_and_verify(USER_INFO['xtest01']['username'], USER_INFO['xtest01']['password'], uri, body, expected_rst, sql_path, yml_path, send_method,setUp={},query=conditions)
                '''.format(module, sub_module, case_name, case_name_eg, setUp, uri, body, conditions, send_method, sql_path, yml_path, expect_rst, function_setup)
    sub_module_file.write(test_script)


def chinese_convert_pingyin(module, sub_module, case_name):
    '''
    将中文转换成拼音
    :param module:
    :param sub_module:
    :param case_name:
    :return:
    '''
    module = pinyin.get(module, format="strip", delimiter="")
    sub_module = 'Test_' + pinyin.get(sub_module, format="strip", delimiter="")
    case_name = pinyin.get(case_name, format="strip", delimiter="")
    return module, sub_module, case_name



# if __name__ == "__main__":
    # 执行pytest单元测试，生成 Allure 报告需要的数据存在 /temp 目录
    # pytest.main(['-s', '-q', r'ExcelInterfaceOpt.py', '--alluredir', './temp'])
#     # 执行命令 allure generate ./temp -o ./report --clean ，生成测试报告
#     os.system('allure generate ./temp -o ../Report --clean')

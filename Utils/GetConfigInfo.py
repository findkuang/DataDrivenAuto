#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/5 23:10
# @Author  : kuangxiaojiang
# @File    : GetConfigInfo.py
# @Function: 获取配置文件信息
import os
import yaml
import datetime
current_dir = os.getcwd()

DB_config_file_path = current_dir + "\\Config\\DB_config.yml"
URL_config_file_path = current_dir + "\\Config\\URL_config.yml"
USER_config_file_path = current_dir + "\\Config\\USER_config.yml"
LOG_config_file_path = current_dir + "\\Config\\LOG_config.yml"
Excel_config_file_path = current_dir + "\\Config\\File_path_list.txt"

# 获取数据库配置文件信息
with open(DB_config_file_path, 'r') as db_config:
    DB_INFO = yaml.full_load(db_config)

# 获取url配置文件信息
with open(URL_config_file_path, 'r') as url_config:
    URL_INFO = yaml.full_load(url_config)

# 获取登录用户配置文件信息
with open(USER_config_file_path, 'r') as user_config:
    USER_INFO = yaml.full_load(user_config)

# 获取日志配置文件信息
with open(LOG_config_file_path, 'r') as log_config:
    LOG_INFO = yaml.full_load(log_config)

# 获取excel路径配置文件信息
with open(Excel_config_file_path, 'r', encoding='utf-8') as excel_path_config:
    EXCEL_PATH_INFO = excel_path_config.readlines()

# 日志文件输出位置和文件名
LOG_FILE_NAME = os.path.join(current_dir, 'Logs', datetime.datetime.now().strftime('%Y-%m-%d') + '.log')
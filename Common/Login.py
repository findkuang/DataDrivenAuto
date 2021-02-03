#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/25 16:13
# @Author  : kuangxiaojiang
# @File    : Login.py
# @Function: 登录功能
from Common.Requests import HttpRquests
from Utils.GetConfigInfo import URL_INFO
from Utils.LoggerHandler import logger
from DB.Singleton import singleton


@singleton
class Login(object):
    def __init__(self, username, pwd):
        self.username = username
        self.password = pwd
        self.access_token, self.req = self.login(username, pwd)
        self.defaultLoc, self.defaultIns = self.get_default_setting(self.req, self.access_token)

    @staticmethod
    def login(username, password):
        '''
        登录
        :return: 返回token，请求对象
        '''
        url = '%s/app-sso/oauth/token?grant_type=password&username=%s&password=%s&verifyCode=&sessionId=' % (URL_INFO['TEST']['url'], username, password)
        headers = {"authorization": "Basic bm9idWc6Z2l2ZW1lZml2ZQ=="}
        req = HttpRquests()
        rst = req.send_post(url, data=None, headers=headers)
        if rst['code'] == 2000:
            logger('登录：').debug('登录成功')
            access_token = rst['body']['access_token']
        else:
            logger('登录').error('登录失败')
            raise AssertionError('登录失败')
        return access_token, req

    @staticmethod
    def get_default_setting(req, access_token):
        '''
        获取默认配置
        :param req: session会话
        :param access_token: token
        :return:
        '''
        url = '%s/app-portal/get/default/setting' % (URL_INFO['TEST']['url'])
        headers = {"Authorization": 'Bearer ' + access_token}
        rst = req.send_post(url, data=None, headers=headers)
        if rst['code'] == 2000:
            defaultLoc = str(rst['body']['defaultLoc'])
            defaultIns = str(rst['body']['defaultIns'])
        else:
            logger('获取默认配置').error('获取默认配置失败')
            raise AssertionError('获取默认配置失败')
        return defaultLoc, defaultIns


if __name__ == "__main__":
    username = 'xtest01'
    pwd = 'A0oX8iipebvaU2OTo07zY9acsFHl1ch%2Bjlb3tbp1RvtD0CTSfUFOwih4A1QspAKOL9q%2B8oOuomMT9nXUBPjGbJRJ5%2BI7R5z946%2BXb5p%2Bxdd%2F0CDvsrlKCU8abkf9HcICyk%2FfHSMShXDEMMzV9eOi8rvZd0JKfbM0lb6tq%2F%2FGnuc%3D'
    lg = Login(username, pwd)
    token, req = lg.login()
    print(token)
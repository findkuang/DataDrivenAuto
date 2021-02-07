#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 17:17
# @Author  : kuangxiaojiang
# @File    : conftest.py.py
# @Function: 用例前置和后置条件
import pytest
from Middle.RequestApi import request_api
from Utils.GetConfigInfo import USER_INFO
from Utils.RandomData import RandomData
from DB.DbAPI import query_db, execute_sql
from Utils.LoggerHandler import logger


def add_user_base_info():
    '''
    前置条件：新增个人档案
    :return:
    '''
    uri = '/app-publichealth/personal/addNewBaseInfo'
    randomData = RandomData()
    formJsonStr = '{\"liveAddress\":{\"city\":\"216449\",\"county\":\"218534\",\"province\":\"191019\",' \
                  '\"town\":\"218535\",\"village\":\"218536\",\"deep\":0,\"value\":\"218536\",\"label\":\"妙山社区\",' \
                  '\"code\":\"331023001040\",\"detailAddress\":\"现住址1\"},\"residenceAddress\":{\"city\":\"216449\",' \
                  '\"county\":\"218534\",\"province\":\"191019\",\"town\":\"218837\",\"village\":\"218844\",' \
                  '\"deep\":0,\"value\":\"218844\",\"label\":\"下洋潘村委会\",\"code\":\"331023105206\",' \
                  '\"detailAddress\":\"户籍地址1\"},\"mgrOrgCode\":\"1\",\"docOrgCode\":\"1\",\"inputOrgCode\":\"1\",' \
                  '\"inputOrgName\":\"浙江大学医学院附属第一医院\",\"responsibleDoctorId\":\"10165\",' \
                  '\"archivingDoctorId\":\"10165\",\"archivingDate\":\"faker.date()\",\"inputDoctorId\":\"10165\",' \
                  '\"inputDoctorName\":\"VV\",\"inputDate\":\"faker.date()\",\"nation\":\"GB/T3304.01\",' \
                  '\"gender\":\"GB/T2261.1.1\",\"isHouseholderReg\":\"1\",\"hasOperations\":[\"0\"],' \
                  '\"hasTraumatisms\":[\"0\"],\"hasTransfusions\":[\"0\"],\"allergySource\":[{\"value\":0,' \
                  '\"isReserveState\":true}],\"exposureHistory\":[{\"value\":0,\"isReserveState\":true}],' \
                  '\"diseases\":[{\"value\":\"FH0369.01\",\"isReserveState\":true,\"diagnosisTime\":\"\"}],' \
                  '\"fatherDiseases\":[{\"value\":\"FH0369.01\",\"isReserveState\":true}],\"motherDiseases\":[{' \
                  '\"value\":\"FH0369.01\",\"isReserveState\":true}],\"childrenDiseases\":[{\"value\":\"FH0369.01\",' \
                  '\"isReserveState\":true}],\"siblingDiseases\":[{\"value\":\"FH0369.01\",\"isReserveState\":true}],' \
                  '\"geneticDiseases\":[{\"value\":0,\"isReserveState\":true}],\"disabilityDiseases\":[{' \
                  '\"value\":\"FH0370.01\",\"isReserveState\":true}],\"lifeEnvKitchenVentList\":[{\"value\":0}],' \
                  '\"lifeEnvFuelTypeList\":[{\"value\":0}],\"lifeEnvWaterList\":[{\"value\":0}],\"lifeEnvWcList\":[{' \
                  '\"value\":0}],\"lifeEnvAnimalList\":[{\"value\":0}],\"gridId\":\"3310\",' \
                  '\"educationLevel\":\"FH0388.02\",\"aboBloodType\":\"CV04.50.005.01\",' \
                  '\"rhBloodType\":\"CV04.50.020.02\",\"maritalStatus\":\"GB/T2261.2.10\",' \
                  '\"careerCate\":\"FH0386.05\",\"hisPayFeeType\":\"FH0368.02\",\"recordDetailCategory\":\"addNew\",' \
                  '\"name\":\"faker.name()\",\"birthday\":\"1990-03-07\",\"idcardNumber\":\"faker.ssn()\",' \
                  '\"phone\":\"faker.phone_number()\",\"workplace\":\"工作单位1\",\"contactsName\":\"faker.name()\",' \
                  '\"contactsPhone\":\"faker.phone_number()\",\"idcardType\":\"FH0066.01\",\"qcResult\":[]} '
    formJsonStr = randomData.random_data_format(formJsonStr)
    body = {"formJsonStr": formJsonStr}
    request_api(USER_INFO['xtest01']['username'], USER_INFO['xtest01']['password'], uri, body)
    return randomData.interface_case_globals


def query_high_risk_diabetes():
    '''
    查询糖尿病高危第一个人id
    :return:
    '''
    sql = "select id as id" \
          "residenter_id as residenterId from biz_ph_high_risk_group_diabetes_info where active = '1' limit 1;"
    rst = query_db(sql)
    return rst[0]


@pytest.fixture()
def case(request):
    '''
    测试用例前置和后置
    :param request:
    :return:
    '''
    caseData = request.param
    if isinstance(caseData, dict):
        setUp = caseData['setUp']
        # 如果有前置条件，则将前置条件的返回结果存取
        if setUp:
            logger('前置条件').debug('【测试前置条件测试】')
            setUp_value = globals()[setUp]()
            request.param['setUp'] = setUp_value
    # 如果是场景类型
    elif isinstance(caseData, list):
        setUp = caseData[0]['setUp']
        # 如果有前置和后置条件，则将前置条件的返回结果存取
        if setUp:
            logger('前置条件').debug('【测试前置条件执行】')
            setUp_value = globals()[setUp]()
            request.param[0]['setUp'] = setUp_value
    return request.param



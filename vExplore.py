#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
import plotly.express as px
from vAPI import main as vapi
import pandas as pd
import concurrent.futures as conc
import time

session = vapi()
slower = 1


def flash():
    print('''

    ||||| CAUTION |||||
    This script is using multithreading and can impact vManage. 
    Define the wait time between each consecutive API calls to 
    vManage [default = 1 sec, to use the default value, just press enter]
    ''')
    while True:
        print('')
        waitTime = input(
            'Please enter the wait time in seconds[default=1]: ')
        print(waitTime)
        try:
            if waitTime == '':
                break
            elif float(waitTime):
                slower = waitTime
                break
            elif int(waitTime):
                slower = waitTime
                break
        except:
            print(' %% Wrong value, please a float or integer number')


flash()


def task1():
    return session.getDataResponse('/dataservice/system/device/vedges')


def task2(data):
    def filter_not_attached(item):
        if item['configOperationMode'] == 'cli':
            return False
        return True
    return list(filter(filter_not_attached, data))


def task2a(rawData):
    dataSet = pd.DataFrame(rawData)
    dataSet1 = dataSet[['deviceType', 'serialNumber', 'uuid', 'chasisNumber', 'deviceModel', 'platformFamily', 'deviceIP', 'site-id', 'host-name', 'template',
                        'templateId']]
    dataSet1.columns = ['deviceType', 'serialNumber', 'uuid', 'chasisNumber', 'deviceModel', 'platformFamily', 'deviceIp', 'siteId', 'hostName', 'deviceTemplateName',
                        'deviceTemplateId']
    return dataSet1


def task3():
    result = session.getDataResponse('/dataservice/template/feature')
    newResult = []
    for item in result:
        if item['devicesAttached'] != 0:
            del item['templateDefinition']
            newResult.append(item)
    return newResult


def task4(item):
    item['deviceTemplates'] = session.getDataResponse(
        f'/dataservice/template/feature/devicetemplates/{item["templateId"]}')
    return item


def task5(item):
    def task_0(t):
        time.sleep(slower)
        t['devices'] = session.getDataResponse(
            f'/dataservice/template/device/config/attached/{t["templateId"]}')
        return t
    with conc.ThreadPoolExecutor() as ex:
        ex.map(task_0, item['deviceTemplates'])
    return item


def makeDF(data):
    return pd.DataFrame(data)


def task6(item):
    view2 = {}
    view2['fTemplateName'] = item['templateName']
    view2['fTemplateType'] = item['templateType']
    view2['deviceType'] = item['templateName']

    for i in item['deviceTemplates']:
        view2['deviceTemplateName'] = i['templateName']
        view2['deviceTemplateId'] = i['templateId']
        for device in i['devices']:
            view2['deviceName'] = device['host-name']
            view2['deviceIp'] = device['deviceIP']
            view2['deviceUUID'] = device['uuid']
            view2['siteId'] = device['site-id']
            dataSet2.append(view2)


def runningTasks():
    idx = 0
    while busy:
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
    return True


print('')
print('==> Collecting Device Data from vManage, please wait ... ')
with conc.ThreadPoolExecutor() as ex:
    print('==> Collecting Device Data')
    r1 = ex.submit(task1).result()
    print('==> Normalizing Device Data')
    r2 = ex.submit(task2, r1).result()
    dataSet1 = ex.submit(task2a, r2).result()
    print('==> Collecting Feature templates Data')
    r3 = ex.submit(task3).result()
    print('==> Collecting Device Template Data')
    r4 = list(ex.map(task4, r3))
    print('==> Referencing Data - if this step fails, increase wait time')
    r5 = list(ex.map(task5, r4))
    dataSet2 = []
    print('==> Finalizing Data normalization')
    r6 = list(ex.map(task6, r5))


def plot(figData):
    fig = px.treemap(data_frame=figData['dataSet'],
                     path=figData['path'], title=figData['title'], hover_name=figData['hoverName'])
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


figData1 = {'dataSet': dataSet1, 'path': [px.Constant('Site ID'),
                                          'siteId', 'deviceTemplateName', 'deviceIp'], 'title': "View 01 - (Site ID) => (Device Template) => (Device)", 'hoverName': 'hostName'}
figData2 = {'dataSet': dataSet1,
            'path': [px.Constant('Device Template Name'), 'deviceTemplateName', 'siteId', 'deviceIp'], 'title': "View 02 - (Device Template) => (Site ID) => (Device)", 'hoverName': 'hostName'}
figData3 = {'dataSet': dataSet1,
            'path': [px.Constant('Device Template Name'), 'deviceTemplateName', 'deviceIp'], 'title': "View 03 - (Device Template) => (Device)", 'hoverName': 'hostName'}
figData4 = {'dataSet': dataSet1,
            'path': [px.Constant('Hadware Family'), 'platformFamily', 'deviceModel', 'siteId', 'deviceIp'], 'title': "View 04 - (Hardware family) => (Device Model) => (Site ID) => (Device)", 'hoverName': 'hostName'}
figData5 = {'dataSet': dataSet1, 'path': [px.Constant('Hardware family'), 'platformFamily', 'deviceModel',
                                          'deviceTemplateName', 'deviceIp'], 'title': "View 05 - (Hardware Family) => (Device Model) => (Device Template) => (Device)", 'hoverName': 'hostName'}
figData6 = {'dataSet': dataSet2,
            'path': [px.Constant('Feature Templates'), 'fTemplateType', 'fTemplateName', 'deviceTemplateName', 'deviceIp'], 'title': "View 06 - (Feature Templates) => (Device Templates) => (Device)", 'hoverName': 'deviceName'}
figData7 = {'dataSet': dataSet2,
            'path': [px.Constant('Device Templates'), 'deviceTemplateName', 'fTemplateType',  'fTemplateName', 'deviceIp'], 'title': "View 07 - (Device Templates) => (Feature Templates) => (Device)", 'hoverName': 'deviceName'}
figData8 = {'dataSet': dataSet2,
            'path': [px.Constant('Device Templates'), 'siteId', 'deviceIp', 'deviceTemplateName', 'fTemplateType', 'fTemplateName'], 'title': "View 08 - (Site ID) => (Device)=> (Device Templates) => (Feature Templates)", 'hoverName': 'deviceName'}


def plotFigure(select):
    switch = {
        1: figData1,
        2: figData2,
        3: figData3,
        4: figData4,
        5: figData5,
        6: figData6,
        7: figData7,
        8: figData8,
    }
    plot(switch.get(select))


def runSelection():
    def banner():
        print('''
    Please Choose one of the following views (enter view number):

    --------------- Site ID and Device Template Name ---------------
    01 - (Site ID) => (Device) => (Device Template)
    02 - (Device Template) => (Site ID) => (Device)
    03 - (Device Template) => (Device)

    ---------------- Hardware and Device Template ------------------
    04 - (Hardware family) => (Device Model) => (Site ID) => (Device)
    05 - (Hardware Family) => (Device Model) => (Device Template) => (Device)

    ---------------------- Feature Templates -----------------------
    06 - (Feature Templates) => (Device Templates) => (Device)
    07 - (Device Templates) => (Feature Templates) => (Device)
    08 - (Site ID) => (Device)=> (Device Templates) => (Feature Templates)
    ----------------------------------------------------------------
    xx - Exit ( ~ type xx or exit)
    ''')

    while True:
        banner()
        print('')
        select = input('   - Please select one of the above views [1-8]: ')
        try:
            if select.lower() == 'exit':
                break
            elif select.lower() == 'xx':
                break
            select = int(select)
            if select > 0 and select <= 8:
                pass
            else:
                print('')
                print('  %% Please enter a value between 1 and 9')
                continue
        except:
            print('')
            print('  %% Wrong selection, please try again')
            continue
        plotFigure(select)


runSelection()

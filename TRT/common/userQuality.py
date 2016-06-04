#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: userQuality.py
@time: 16/5/19 下午3:50
@description: null
"""
from datetime import datetime
from config import config
from lib import stdLib


def userQuality(functionName='lifeTime'):
    if functionName == 'lifeTime':
        lifeTime()

def lifeTime():
    filename = config.ratingWithLabelFile
    read = open(filename, 'r')
    data = read.readlines()
    read.close()

    userDict = dict()
    maxTime = datetime.utcfromtimestamp(0)
    initTime = datetime.utcnow()
    resultDict = dict()

    for i in data:
        tmp = i[:-1].split(config.separator)
        userId = tmp[0]
        time = datetime.utcfromtimestamp(float(tmp[3]))
        userDict.setdefault(userId, {'max': maxTime, 'min': initTime, 'freq': 0})
        if time > userDict[userId]['max']:
            userDict[userId]['max'] = time
        if time < userDict[userId]['min']:
            userDict[userId]['min'] = time
        userDict[userId]['freq'] += 1
    # count = 0
    # max = 0
    # min = 1
    for i in userDict:
        resultDict.setdefault(i, 0)
        day = userDict[i]['max'] - userDict[i]['min']
        # if day.days() == 0:
        #     print day
        #     resultDict[i] = 0
        #     count += 1
        # else:
        resultDict[i] = day.days
    #     if resultDict[i] > max:
    #         max = resultDict[i]
    #     if resultDict[i] < min:
    #         min = resultDict[i]
    # print resultDict
    #
    # for i in resultDict:
    #     resultDict[i] = (resultDict[i] - min) / (max - min)
    # print resultDict

    outfile = config.userQualityDict
    stdLib.dumpData(resultDict, outfile)

#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.io
@software: PyCharm
@file: reduceByTag.py
@time: 16/7/7 下午1:31
@description: null
"""
from config import config

def reduceByTag():
    divideByK()

def divideByK(filename=config.metaRatingFile_10m):
    data = readFile(filename)
    length = len(data)
    count = 0
    k = 1
    resultDict = dict()
    userDict = dict()
    for i in data:
        count += 1
        tmp = i[:-1].split(config.separator)
        userId = tmp[0]

        if count > 1000005 and userId not in userDict:
            print count
            count = 0
            k += 1
            continue
        userDict.setdefault(userId, 0)
        resultDict.setdefault(k, list())
        resultDict[k].append(i)

    for k in resultDict:
        fileName = 'result/reducedMetaRatings%d.txt' % k
        out = open(fileName, 'w')
        for i in resultDict[k]:
            out.write(i)
        out.close()

def readFile(filename=config.metaRatingFile):
    read = open(filename, 'r')
    data = read.readlines()
    read.close()
    return data
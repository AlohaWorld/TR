#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: highPrecisionUserAnalysis.py
@time: 16/5/31 上午10:46
@description: null
"""
from config import config
from lib import stdLib

def highPrecisionUserAnalysis():
    filename = config.ratingWithLabelFile
    read = open(filename)
    data = read.readlines()
    read.close()

    ratingTimesDict = dict()
    userQualityDict = stdLib.loadData(config.userQualityDict)

    for line in data:
        tmp = line[:-1].split(config.separator)
        userId = tmp[0]
        ratingTimesDict.setdefault(userId, 0)
        ratingTimesDict[userId] += 1

    outFile = "precisionWithRatingTimes.txt"
    out = open(outFile, 'w')
    precisionFile = open("precisionFile.txt")
    for line in precisionFile.readlines():
        tmp = line[:-1].split(config.separator)
        userId = tmp[0]
        tmp.append(str(ratingTimesDict[userId]))
        tmp.append(str(userQualityDict[userId]))
        out.write(config.separator.join(tmp) + '\n')
    out.close()

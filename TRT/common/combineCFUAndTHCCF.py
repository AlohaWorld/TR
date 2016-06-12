#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: combineCFUAndTHCCF.py
@time: 16/1/18 17:30
@description: null
"""
from config import config
from lib import stdLib

def combine():
    CFUData = stdLib.loadData(config.CFUUserSimMatrix)  # (config.SVDUserSimMatrix)  #
    simData = stdLib.loadData(config.userSimMatrix)
    print 'start combining CFU and sim......'
    CFUDict = {}
    simDict = {}
    resultDict = {}
    for user in CFUData:
        CFUDict.setdefault(user, {})
        for tuples in CFUData[user]:
            CFUDict[user].setdefault(tuples[0], tuples[1])
        simDict.setdefault(user, {})
        for tuples in simData[user]:
            simDict[user].setdefault(tuples[0], tuples[1])

    for user in CFUDict:
        for simUser in CFUDict[user]:
            if simUser in simDict[user]:
                CFUDict[user][simUser] = CFUDict[user][simUser] * config.alpha + \
                                         simDict[user][simUser] * (1 - config.alpha)
            else:
                CFUDict[user][simUser] *= config.alpha
        for simUser in simDict[user]:
            CFUDict[user].setdefault(simUser, simDict[user][simUser] * (1 - config.alpha))

        sortedRecommand = sorted(CFUDict[user].iteritems(), key=lambda d: d[1], reverse=True)
        resultDict.setdefault(user, [])
        for i in sortedRecommand:
            resultDict[user].append(i)

    stdLib.dumpData(resultDict, config.combineSimMatrix)
    print 'combine finished......'
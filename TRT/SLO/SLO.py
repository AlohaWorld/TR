#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.io
@software: PyCharm
@file: SLO.py
@time: 16/6/15 下午9:05
@description: null
"""
import time
from lib import stdLib
from config import config

class SLO(object):
    def __init__(self):
        self.uiDict = stdLib.loadData(config.uiDictFile)

    def sloMatrix(self, filtrate=5):
        """
        uiDict: user_item download record, datatype: dictionary of dictionary of int
        filtrate: the criteria of filting users and items, datatype: int
        return datatype: dictionary of dictionary of tuple,[0] is deviation [2] is weight
        """
        computeMethod = self.scoredMethod
        matrixDict = dict()
        itemSet = set()
        userDict = dict()
        for user in self.uiDict:
            history = set(self.uiDict[user].keys())
            if len(history) < filtrate:
                continue
            itemSet.update(history)
            userDict[user] = self.uiDict[user]
        print 'item', len(itemSet), 'user', len(userDict)
        PROCESS = len(itemSet)
        COUNTER = 0.0
        for i in itemSet:
            COUNTER += 1
            matrixDict[i] = dict()
            for j in itemSet:
                if i == j:
                    continue
                resultTuple = computeMethod(userDict, i, j)
                if resultTuple[1] != 0:
                    matrixDict[i][j] = resultTuple
            print '\r%.1f' % (100 * COUNTER / PROCESS) + '%', '--', '%.3f' % time.clock(), 's',
        print ''
        stdLib.dumpData(matrixDict, config.SLOMatrix)

    def scoredMethod(self, userDict, former, later):
        deviation = 0.0
        weight = 0
        for user in userDict:
            temp = userDict[user]
            if former not in temp or later not in temp:
                continue
            deviation += temp[later] - temp[former]
            weight += 1
        if weight != 0:
            deviation /= weight
        resultTuple = deviation, weight
        return resultTuple

    def generateRecommend(self):
        sloMatrix = stdLib.loadData(config.SLOMatrix)
        count = 0
        length = len(sloMatrix)
        recommendList = dict()
        for user in self.uiDict:
            count += 1
            recommendList.setdefault(user, list())
            history = self.uiDict[user]
            resultList = []
            for i in sloMatrix:
                if i in history:
                    continue
                score = 0.0
                weight = 0.0
                for j in history:
                    if j in sloMatrix[i]:
                        temp = sloMatrix[j][i]
                        score += (history[j] + temp[0]) * temp[1]
                        weight += temp[1]
                if weight != 0:
                    resultList.append((i, score))
            resultList.sort(key=self.sortKey, reverse=True)
            recommendList[user] = resultList[0:config.listLength]
            print '\r%.1f' % (100 * count / length) + '%', '--', '%.3f' % time.clock(), 's',
        outfile = config.SLORecommendListFile
        out = open(outfile, 'w')
        for i in recommendList:
            tmp = ""
            for j in recommendList[i]:
                tmp = tmp + j[0] + config.subSeparator
            out.write(i + config.separator + tmp[:-1] + '\n')
        out.close()

    def sortKey(self, tupl):
        return tupl[1]

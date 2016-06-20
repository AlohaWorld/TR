#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: UHCF.py
@time: 15/12/7 15:16
@description: null
"""
from datetime import datetime
import heapq
import time
from config import config
from math import sqrt, log, e
from lib import stdLib

class TRT(object):
    def __init__(self):
        self.userDict = dict()  # 用于存放用户及其偏好的dictionary
        self.userPreferRateDict = dict()  # 用于存放用户及其各个标签偏好比率的dictionary
        self.timeIntervalDict = dict()
        self.now = datetime(2016, 5, 17)  # datetime.utcnow()
        self.userQualityDict = stdLib.loadData(config.userQualityDict)

    # 生成用户偏好的函数
    def generaUserPrefer(self):
        print 'UHCF starting...'
        ratings = open(config.ratingWithLabelFile)
        data = ratings.readlines()
        length = len(data)
        ratings.close()

        count = 0.0
        for i in data:
            count += 1
            self.labelPreferCal(i)  # 根据打分时间进行惩罚
            print '\r%.1f' % (100 * count / length) + '%', '--', '%.3f' % time.clock(), 's',

        # filename = "test.txt"
        # out = open(filename, 'w')
        # for i in self.userDict:
        #     for j in range(config.labelLength):
        #         out.write(i + config.separator + str(j) + config.separator + str(self.userDict[i][j]) + "\n")
        # out.close()
        # 对用户标签偏好进行归一化
        for i in self.userDict:
            maxV = minV = self.userDict[i][0]
            for j in range(config.labelLength):
                if self.userDict[i][j] > maxV:
                    maxV = self.userDict[i][j]
                if self.userDict[i][j] < minV:
                    minV = self.userDict[i][j]
            if minV == maxV:
                continue
            for j in range(config.labelLength):
                self.userDict[i][j] = (self.userDict[i][j] - minV) / (maxV - minV)

        outfile = config.userPreferFile
        out = open(outfile, 'w')
        for i in self.userDict:
            result = ""
            for j in range(config.labelLength):
                if j in self.userDict[i]:
                    result += str(self.userDict[i][j]) + config.subSeparator
                else:
                    result += '0|'
            out.write(i + config.separator + result[:-1] + '\n')
        out.close()

        print 'finished...'
        return 0

    def labelPreferCal(self, line):
        tmp = line[:-1].split(config.separator)
        userId = tmp[0]
        grade = float(tmp[2])
        rateTime = datetime.utcfromtimestamp(float(tmp[3]))
        T = (self.now - rateTime).days  # 不进行时间窗口的移动,将打分时间距今的时间转换为天数
        labels = tmp[4]
        labelArr = labels.split(config.subSeparator)
        labelLen = 0  # 电影所含的标签数量
        for i in labelArr:
            if i == '1':
                labelLen += 1

        aGrade = grade / labelLen  # 每个标签的平均得分 TODO:按照用户以前生成的偏好对不同标签进行偏置

        self.userDict.setdefault(userId, {})

        # 对每个标签进行time hot算法的计算,得出每个标签的得分
        for j in range(config.labelLength):
            self.userDict[userId].setdefault(j, 0)
            if labelArr[j] == '1':
                self.userDict[userId][j] += aGrade  # / pow(T, config.G)
                # / log(T - self.userQualityDict[userId] * config.beta, e)

    def utDictGenerate(self):
        read = open(config.userPreferFile, 'r')
        data = read.readlines()
        print "generating ut dict......"
        result = dict()
        for i in data:
            tmp = i[:-1].split(config.separator)
            userId = tmp[0]
            tags = tmp[1].split(config.subSeparator)
            result.setdefault(userId, {})
            for j in range(config.labelLength):
                result[userId].setdefault(j, float(tags[j]))
        stdLib.dumpData(result, config.utDictFile)

    def matrix(self, utDict = None, filtrate = 5):
        '''
        calaulate the item_similarity matrix, using given simialrity method
        :param uiDict: user-item score table, data type: dict
        :threshold: qualifying the neighbour users,data type: float
        :filtrate: the criteria of filting users, data type: int
        '''
        print 'calculating the user matrix......'
        utDict = utDict or stdLib.loadData(config.utDictFile)
        matrixDict = dict()
        PROCESS = len(utDict)
        COUNTER = 0.0
        for i in utDict:
            COUNTER += 1
            vec1 = utDict[i]
            if len(vec1) < filtrate:
                continue
            for j in utDict:
                if i == j:
                    continue
                vec2 = utDict[j]
                if len(vec2) < filtrate:
                    continue
                similarity = self.adjustedCosine(vec1, vec2)
                if similarity > 0:
                    matrixDict.setdefault(i, list())
                    matrixDict[i].append((j, similarity))
            if i in matrixDict:
                matrixDict[i] = heapq.nlargest(config.n, matrixDict[i], key=lambda x: x[1])

            print '\r%.1f' % (100 * COUNTER / PROCESS) + '%', '--', '%.3f' % time.clock(), 's',
        outfile = config.userSimMatrix
        stdLib.dumpData(matrixDict, outfile)

    def adjustedCosine(self, vec1, vec2):
        su = 0.0
        l1 = 0.0
        l2 = 0.0
        avg1 = sum([vec1[i] for i in vec1]) / float(len(vec1))
        avg2 = sum([vec2[i] for i in vec2]) / float(len(vec2))
        for i in vec1:
            if i in vec2:
                su += (vec1[i] - avg1) * (vec2[i] - avg2)
                l1 += pow((vec1[i] - avg1), 2)
                l2 += pow((vec2[i] - avg2), 2)
        temp = l1 * l2
        if temp != 0:
            similarity = su / sqrt(temp)
        else:
            similarity = 0
        return similarity
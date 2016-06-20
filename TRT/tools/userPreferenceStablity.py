#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.io
@software: PyCharm
@file: userPreferenceStablity.py
@time: 16/6/15 下午10:02
@description: null
"""
from config import config
import time
from lib import stdLib
from datetime import datetime


class UserPreferenceStablity(object):
    def __init__(self):
        self.userDict = dict()  # 用于存放用户及其偏好的dictionary
        self.userPreferRateDict = dict()  # 用于存放用户及其各个标签偏好比率的dictionary
        self.now = datetime(2016, 5, 17)  # datetime.utcnow()

        filename = config.ratingWithLabelFile
        read = open(filename, 'r')
        self.data = read.readlines()
        read.close()

        self.countRating = dict()

        # self.userFirstRating()
        self.userFirstRatingDict = stdLib.loadData(config.userFirstRatingDict)

    def userFirstRating(self):

        resultDict = dict()

        for i in self.data:
            tmp = i[:-1].split(config.separator)
            userId = tmp[0]
            time = datetime.utcfromtimestamp(float(tmp[3]))
            resultDict.setdefault(userId, time)
            if time < resultDict[userId]:
                resultDict[userId] = time

        outfile = config.userFirstRatingDict
        stdLib.dumpData(resultDict, outfile)

    # 生成用户偏好的函数
    def generaUserPrefer(self):
        print 'user rating preference stablity calculation starting...'
        length = len(self.data)

        count = 0.0
        for i in self.data:
            count += 1
            self.labelPreferCal(i)  # 根据打分时间进行惩罚
            print '\r%.1f' % (100 * count / length) + '%', '--', '%.3f' % time.clock(), 's',
        # 对用户标签偏好进行归一化
        for i in self.userDict:
            for j in self.userDict[i]:
                maxV = minV = self.userDict[i][j][0]
                for k in range(1, config.labelLength):
                    if self.userDict[i][j][k] > maxV:
                        maxV = self.userDict[i][j][k]
                    if self.userDict[i][j][k] < minV:
                        minV = self.userDict[i][j][k]
                if minV == maxV:
                    continue
                for k in range(config.labelLength):
                    self.userDict[i][j][k] = (self.userDict[i][j][k] - minV) / (maxV - minV)
        stdLib.dumpData(self.userDict, config.userStablityDict)

        print 'finished...'

    # 计算用户评分偏好稳定性
    def calStablity(self):
        userDict = stdLib.loadData(config.userStablityDict)
        print userDict['195']
        for user in userDict:
            result = sorted(userDict[user].items(), key=lambda x: x[0], reverse=True)
            self.userPreferRateDict.setdefault(user, 0)
            gap = 0
            count = 1
            for prefer in range(1, len(result)):
                count += 1
                for k in range(config.labelLength):
                    gap += abs(result[prefer - 1][1][k] - result[prefer][1][k])
            self.userPreferRateDict[user] = gap / (count * config.labelLength)
        print sorted(self.userPreferRateDict.items(), key=lambda x: x[1], reverse=True)

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

        if userId not in self.userDict:
            self.countRating.setdefault(userId, 0)
        self.userDict.setdefault(userId, dict())
        if (rateTime - self.userFirstRatingDict[userId]).days > config.stableTime:
            self.userFirstRatingDict[userId] = rateTime
            # 对每个标签进行time hot算法的计算,得出每个标签的得分
            self.countRating[userId] += 1
            self.userDict[userId].setdefault(self.countRating[userId], dict())
            # 对每个标签进行time hot算法的计算,得出每个标签的得分
            for j in range(config.labelLength):
                self.userDict[userId][self.countRating[userId]].setdefault(j, 0)
                if labelArr[j] == '1':
                    self.userDict[userId][self.countRating[userId]][j] += aGrade
        else:
            self.userDict[userId].setdefault(self.countRating[userId], dict())
            # 对每个标签进行time hot算法的计算,得出每个标签的得分
            for j in range(config.labelLength):
                self.userDict[userId][self.countRating[userId]].setdefault(j, 0)
                if labelArr[j] == '1':
                    self.userDict[userId][self.countRating[userId]][j] += aGrade



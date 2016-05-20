#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: evaluation.py
@time: 16/1/6 17:23
@description: null
"""
from config import config
import math
from lib import stdLib

class Evaluation(object):
    def __init__(self, filename=None):
        resultFile = filename or config.recommendListFile
        result = open(resultFile).readlines()
        test = open(config.testFile).readlines()
        self.resultData = {}
        self.testData = {}
        for i in result:
            tmp = i[:-1].split(config.separator)
            userId = tmp[0]
            recommendList = tmp[1].split(config.subSeparator)
            self.resultData.setdefault(userId, recommendList)
        for i in test:
            tmp = i[:-1].split(config.separator)
            userId = tmp[0]
            movieId = tmp[1]
            grade = float(tmp[2])
            self.testData.setdefault(userId, dict())
            self.testData[userId].setdefault(movieId, grade)


    def recall_and_precision(self):
        """
        Get the recall and precision
        """
        result = self.resultData
        test = self.testData
        hit = 0
        recall = 0
        precision = 0
        for user in result.keys():
            tu = test.get(user, {})
            for item in result[user]:
                if item in tu:
                    hit += 1
            recall += len(tu)
            precision += config.listLength

        recall = hit * 100 / (recall * 1.0)
        precision = hit * 100 / (precision * 1.0)
        if recall != 0 and precision != 0:
            return [recall, precision]
        else:
            return [0, 0]

    def fvalue(self, rap=None):  # rap意思是recall and precision
        if rap[0] == 0 and rap[1] == 0:
            return 0
        return rap[0] * rap[1] * 2 / (rap[0] + rap[1])
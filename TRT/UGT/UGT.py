#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: UGT.py
@time: 16/6/12 下午6:08
@description: null
"""
from lib import stdLib
import heapq
from config import config

class UGT(object):
    def __init__(self):
        self.user_tags = dict()
        self.tag_items = dict()
        self.user_items = dict()
        test = open(config.testFile).readlines()
        self.resultData = {}
        self.testData = {}
        for i in test:
            tmp = i[:-1].split(config.separator)
            userId = tmp[0]
            movieId = tmp[1]
            grade = float(tmp[2])
            self.testData.setdefault(userId, dict())
            self.testData[userId].setdefault(movieId, grade)

    # 统计各类数量
    def addValueToMat(self, theMat, key, value, incr):
        if key not in theMat:  # 如果key没出先在theMat中
            theMat[key] = dict()
            theMat[key][value] = incr
        else:
            if value not in theMat[key]:
              theMat[key][value] = incr
            else:
              theMat[key][value] += incr  # 若有值，则递增

    # 初始化，进行各种统计
    def initStat(self):
        print "initializing......"
        read = open(config.metaTagFile)
        data = read.readlines()
        read.close()

        for i in data:
            tmp = i[:-1].split(config.separator)
            user = tmp[0]
            movie = tmp[1]
            tag = tmp[2]
            self.addValueToMat(self.user_tags, user, tag, 1)
            self.addValueToMat(self.user_items, user, movie, 1)
            self.addValueToMat(self.tag_items, tag, movie, 1)
        print "finished......"

    def generateRecommend(self):
        print "generating recommendation......"
        result = dict()
        self.resultData = dict()
        length = len(self.user_items)
        count = 0
        for user in self.user_items:
            count += 1
            tmp = self.recommend(user)
            result.setdefault(user, list())
            self.resultData.setdefault(user, dict())
            result[user] = sorted(tmp.items(), key=lambda x: x[1], reverse=True)[:config.listLength]
            for i in result[user]:
                self.resultData[user].setdefault(i[0], i[1])
            print self.resultData[user]
            if count % int(length * config.percentage) == 0:
                print '%f%%' % (count * 100 / length)

    # 推荐算法
    def recommend(self, usr):
        recommend_list = dict()
        tagged_item = self.user_items[usr]  # 得到该用户所有推荐过的物品
        for tag, wut in self.user_tags[usr].items():  # 用户打过的标签及次数
            for item, wit in self.tag_items[tag].items():  # 物品被打过的标签及被打过的次数
                if item not in tagged_item:  # 已经推荐过的不再推荐
                    continue
                if item not in recommend_list:
                    recommend_list[item] = wut * wit  # 根据公式
                else:
                    recommend_list[item] += wut * wit
        return recommend_list

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
            # if len(tu) == 0:
            #     print tu
            #     continue
            for item in result[user]:
                if item in tu:
                    hit += 1
            recall += len(tu)
            precision += len(result[user])

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
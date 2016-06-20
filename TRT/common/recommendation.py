#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: recommendation.py
@time: 16/1/18 14:27
@description: null
"""
from config import config
from lib import stdLib
import time

def generaRecommendList(simMatrix = None):
    filename = simMatrix or config.CFUUserSimMatrix
    simUsers = stdLib.loadData(filename)
    length = len(simUsers)

    uiDict = stdLib.loadData(config.uiDictFile)
    recommendDict = dict()
    count = 0
    print 'generating recommend list......'
    for user in simUsers:
        count += 1
        if user not in uiDict:
            continue
        history = uiDict[user]
        recommendDict.setdefault(user, dict())
        for simUser in simUsers[user]:  # simUsers是用户相似度矩阵,candidate是与userId相似的用户及其相似度
            tmpUser = simUser[0]
            similarity = simUser[1]
            if tmpUser in uiDict:
                candidate = uiDict[tmpUser]
                for item in candidate:
                    if item in history:
                        continue
                    rating = candidate[item]
                    recommendDict[user].setdefault(item, 0)
                    recommendDict[user][item] += float(similarity) * rating
        recommendDict[user] = dict(sorted(recommendDict[user].items(),
                                            key=lambda x: x[1], reverse=True)[0:config.listLength])
        print '\r%.1f' % (100 * count / length) + '%', '--', '%.3f' % time.clock(), 's',
    print 'writing data......'
    outfile = config.recommendListFile
    out = open(outfile, 'w')
    for i in recommendDict:
        out.write(i + config.separator + config.subSeparator.join(recommendDict[i]) + '\n')
    out.close()
    outfile = config.recommendDict
    stdLib.dumpData(recommendDict, outfile)

#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: settleSVDData.py
@time: 16/5/23 下午8:52
@description: null
"""
from UHCF.config import config
from UHCF.lib import stdLib

def settleSVDData():
    SVDData = stdLib.loadData(config.SVDUserSimDict)
    SVDDict = dict()
    for user in SVDData:
        for tuples in SVDData[user]:
            SVDDict.setdefault(str(user), list())
            SVDDict[str(user)].append((str(tuples[0]), tuples[1]))
    outfile = config.SVDSettledUserSimDict
    stdLib.dumpData(SVDDict, outfile)


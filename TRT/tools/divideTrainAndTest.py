#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: divideTrainAndTest.py
@time: 16/1/6 15:29
@description: null
"""
from config import config
from lib import stdLib
import os
from random import randint, shuffle


def readFile(filename=config.metaRatingFile):
    read = open(filename, 'r')
    data = read.readlines()
    read.close()
    return data

def divideTrainAndTest(fileID, name = 'time'):
    print 'spliting data......'
    if name == 'time':
        divideByTime(True)
    elif name == 'user':
        divideByUser()
    elif name == 'random':
        divideByRandom(fileID)
    elif name == 'k':
        divideByK()
    settleUIAndIU()

    print "Data split finished..."

def divideByTime(delete = False, filename=config.metaRatingFile):
    data = readFile(filename)
    if delete is False:
        notDeleteDataByTime(data)
    else:
        deleteDataByTime(data)

def notDeleteDataByTime(data):
    trainData = []
    testData = []
    for i in data:
        tmp = i[:-1].split(config.separator)
        time = tmp[3]
        if float(time) > 975804787:
            testData.append(i)
        else:
            trainData.append(i)
    print len(trainData)
    print len(testData)

    writeFile(trainData, testData)

def deleteDataByTime(data):
    trainDict = dict()
    testDict = dict()
    trainData = []
    testData = []
    for i in data:
        tmp = i[:-1].split(config.separator)
        userId = tmp[0]
        time = tmp[3]
        if float(time) > 975804787:
            testDict.setdefault(userId, [])
            testDict[userId].append(i)
        else:
            trainDict.setdefault(userId, [])
            trainDict[userId].append(i)
    for i in trainDict:
        if i in testDict:
            for j in range(len(trainDict[i])):
                trainData.append(trainDict[i][j])
    for i in testDict:
        if i in trainDict:
            for j in range(len(testDict[i])):
                testData.append(testDict[i][j])
    print len(trainData)
    print len(testData)
    writeFile(trainData, testData)

def divideByUser(filename=config.metaRatingFile):
    trainData = []
    testData = []
    count = 0
    data = readFile(filename)
    for i in data:
        count += 1
        if count % 5 == 0:
            testData.append(i)
        else:
            trainData.append(i)
    print len(trainData)
    print len(testData)

    writeFile(trainData, testData)

def divideByRandom(fileID, filename=config.metaShuffledFile):
    shuffleFile(fileID)
    trainData = []
    testData = []
    count = 0
    data = readFile(filename)
    for i in data:
        count += 1
        if count % 5 == 0:
            testData.append(i)
        else:
            trainData.append(i)
    print len(trainData)
    print len(testData)

    writeFile(trainData, testData)

def settleUIAndIU():
    file = open(config.trainFile, 'r')
    data = file.readlines()
    uiDict = dict()
    iuDict = dict()
    for i in data:
        tmp = i[:-1].split(config.separator)
        userId = tmp[0]
        movieId = tmp[1]
        rating = float(tmp[2])
        uiDict.setdefault(userId, dict())
        iuDict.setdefault(movieId, dict())
        uiDict[userId].setdefault(movieId, rating)
        iuDict[movieId].setdefault(userId, rating)
    stdLib.dumpData(uiDict, config.uiDictFile)
    stdLib.dumpData(iuDict, config.iuDictFile)

def writeFile(trainData, testData):
    trainOut = open(config.trainFile, 'w')
    trainOut.write(''.join(trainData))
    trainOut.close()
    testOut = open(config.testFile, 'w')
    testOut.write(''.join(testData))
    testOut.close()

def shuffleFile(fileID):
    filename = r'result/reducedMetaRatings%d.txt' % fileID
    read = open(filename, 'r')
    data = read.readlines()
    read.close()
    out = open(config.metaShuffledFile, 'w')
    shuffle(data)
    out.writelines(data)
    out.close()

def divideByK(filename=config.metaShuffledFile):
    shuffleFile()
    data = readFile(filename)
    length = len(data)
    count = 0
    k = 1
    resultDict = dict()
    for i in data:
        count += 1
        resultDict.setdefault(k, [])
        resultDict[k].append(i)
        if count == length / config.divideK:
            count = 0
            k += 1
    for k in resultDict:
        trainFileName = 'result/trainRatings%d.txt' % k
        testFileName = 'result/testRatings%d.txt' % k
        out1 = open(trainFileName, 'w')
        out2 = open(testFileName, 'w')
        for i in resultDict[k]:
            rand = randint(1, 5)
            if rand == 5:
                out2.write(i)
            else:
                out1.write(i)
        out1.close()
        out2.close()

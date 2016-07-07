#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: run.py
@time: 16/1/5 21:43
@description: null
"""
from datetime import datetime
from os import path
from tools.sortByTime import sortByTime
from tools.combineById import combineById
from tools.divideTrainAndTest import divideTrainAndTest
from tools.transRating import transRating
from tools.highPrecisionUserAnalysis import highPrecisionUserAnalysis
from tools.userPreferenceStablity import UserPreferenceStablity
from CFU.CFU import CFU
from core.TRT import TRT
from UGT.UGT import UGT
from SLO.SLO import SLO
from common.evaluation import Evaluation
from common.recommendation import generaRecommendList
from common.combineCFUAndTHCCF import combine
from common.userQuality import userQuality
from config import config
from reduce10mData import reduceByTag

def evaluate(algoType):
    if config.needEvaluate is True:
        if config.needCombine is False:
            config.alpha = 0
        if config.needSLO is True:
            evaluate = Evaluation(config.SLORecommendListFile)
        else:
            evaluate = Evaluation()
        # evaluate.find_great_recommendation()
        # highPrecisionUserAnalysis()
        rap = evaluate.recall_and_precision()
        print "recall: %5.5f%%" % rap[0]
        print "precision: %5.5f%%" % rap[1]
        fvalue = evaluate.fvalue(rap)
        print "F value: %5.5f%%" % fvalue
        mae = 0
        print "MAE: %5.5f" % mae
        outfile = r'evaluation/evaluationResult.csv'
        out = open(outfile, 'a')
        spliter = ','
        out.write(str(config.n) + spliter + str(config.listLength) +
                  spliter + str(config.G) + spliter + str(config.delta) +
                  spliter + str(config.alpha) + spliter + str(rap[0])[:7] + '%' + spliter + str(rap[1])[:7] +
                  '%' + spliter + str(fvalue)[:7] + '%' + spliter + str(mae)[:7] + spliter + algoType + spliter + '\n')
        out.close()

def generateRecList(algoType = 'TRT'):
    while (config.listLength <= 100):
        if algoType is 'TRT':
            generaRecommendList(config.userSimMatrix)
        if algoType is 'CFU':
            generaRecommendList()
        evaluate(algoType)
        config.listLength += 10

if __name__ == '__main__':
    startTime = datetime.now()
    print 'program start......'
    print 'start time :'
    print startTime
    if path.exists('result/reducedMetaRatings1.txt') is False:
        print 'Dividing meta data......'
        reduceByTag.reduceByTag()  # 划分10m数据集为10个1m数据集
    k = 1
    while (k < 10):
        if config.needDivideTrainAndTest is True:
            divideTrainAndTest(k, config.divideMethod)
        if config.needPreSettle is True:
            sortByTime()
            combineById()
            userQuality()
        if config.needUPS is True:
            ups = UserPreferenceStablity()
            ups.generaUserPrefer()
            ups.calStablity()
        if config.needTRT is True:
            trt = TRT()
            trt.generaUserPrefer()
            trt.utDictGenerate()
            trt.matrix()
            generateRecList()
        if config.needCFU is True:
            cfu = CFU()
            cfu.matrix()
            generateRecList('CFU')
        if config.needCombine is True:
            combine()
            generaRecommendList(config.combineSimMatrix)
        if config.needUGT is True:
            ugt = UGT()
            ugt.initStat()
            ugt.generateRecommend()
            rap = ugt.recall_and_precision()
            print "recall: %5.5f%%" % rap[0]
            print "precision: %5.5f%%" % rap[1]
            fvalue = ugt.fvalue(rap)
            print "F value: %5.5f%%" % fvalue
        if config.needSLO is True:
            slo = SLO()
            slo.sloMatrix()
            while (config.listLength <= 100):
                slo.generateRecommend()
                evaluate('SLO')
                config.listLength += 10
        k += 2
    endTime = datetime.now()
    print 'program finished......'
    print 'finish time :'
    print endTime
    print 'total run time :'
    print endTime - startTime


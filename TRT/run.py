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
from tools.sortByTime import sortByTime
from tools.combineById import combineById
from tools.divideTrainAndTest import divideTrainAndTest
from CFU.CFU import CFU
from core.TRT import TRT
from common.evaluation import Evaluation
from common.recommendation import generaRecommendList
from common.combineCFUAndTHCCF import combine
from config import config

if __name__ == '__main__':
    startTime = datetime.now()

    print 'program start......'
    print 'start time :'
    print startTime
    if config.needDivideTrainAndTest is True:
        divideTrainAndTest()
    if config.needPreSettle is True:
        sortByTime()
        combineById()
    if config.needTRT is True:
        trt = TRT()
        trt.generaUserPrefer()
        trt.simCalculate()
        if config.needCombine is False and config.needCFU is False:
            generaRecommendList(config.userSimMatrix)
    if config.needCFU is True:
        cfu = CFU()
        cfu.matrix()
        if config.needCombine is False and config.needTRT is False:
            generaRecommendList()
    if config.needCombine is True:
        combine()
        generaRecommendList(config.combineSimMatrix)
    if config.needEvaluate is True:
        evaluate = Evaluation()
        rap = evaluate.recall_and_precision()
        print "recall: %5.5f%%" % rap[0]
        print "precision: %5.5f%%" % rap[1]
        fvalue = evaluate.fvalue(rap)
        print "F value: %5.5f%%" % fvalue
        mae = 0
        print "MAE: %5.5f" % mae
        outfile = r'result/evaluationResult.csv'
        out = open(outfile, 'a')
        spliter = ','
        out.write(str(config.n) + spliter + str(config.listLength) +
                  spliter + str(config.G) + spliter + str(config.delta) +
                  spliter + str(rap[0])[:7] + '%' + spliter + str(rap[1])[:7] +
                  '%' + spliter + str(fvalue)[:7] + '%' + spliter + str(mae)[:7] + spliter + '\n')
        out.close()
    endTime = datetime.now()
    print 'program finished......'
    print 'finish time :'
    print endTime
    print 'total run time :'
    print endTime - startTime

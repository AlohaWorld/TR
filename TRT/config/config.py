#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: config.py
@time: 16/1/5 17:48
@description: null
"""
from os import path
from sys import argv
from ConfigParser import ConfigParser

conf = ConfigParser()
conf.read('config/config.ini')


# 文件各项之间的分隔符
separator = conf.get('mainconf', 'separator')
subSeparator = conf.get('mainconf', 'subseparator')

# meta file为元数据文件存放的位置
metaRatingFile = path.join(path.dirname(argv[0]), r'result/reducedMetaRatings1.txt')  # path.join(path.dirname(argv[0]), conf.get('fileconf', 'metaRatingFile'))
metaMovieFile = path.join(path.dirname(argv[0]), conf.get('fileconf', 'metaMovieFile'))
metaRatingFile_10m = path.join(path.dirname(argv[0]), conf.get('fileconf', 'metaRatingFile_10m'))
metaMovieFile_10m = path.join(path.dirname(argv[0]), conf.get('fileconf', 'metaMovieFile_10m'))
metaTagFile_10m = path.join(path.dirname(argv[0]), conf.get('fileconf', 'metaTagFile_10m'))
metaShuffledFile = path.join(path.dirname(argv[0]), r'result/metaShuffledFile.txt')
metaTagFile = path.join(path.dirname(argv[0]), r'result/metaTagFile')

# 训练集和测试集
trainFile = path.join(path.dirname(argv[0]), r'result/trainRatings.txt')
testFile = path.join(path.dirname(argv[0]), r'result/testRatings.txt')
uiDictFile = path.join(path.dirname(argv[0]), r'result/uiDict.dict')
utDictFile = path.join(path.dirname(argv[0]), r'result/utDict.dict')
iuDictFile = path.join(path.dirname(argv[0]), r'result/iuDict.dict')
# sorted file为将元数据按照时间先后顺序排列的文件
sortedRatingFile = path.join(path.dirname(argv[0]), r'result/sortedRatings.txt')

# label file为将排序后的文件后面接上对应电影的label生成的文件
ratingWithLabelFile = path.join(path.dirname(argv[0]), r'result/ratingWithLabels.txt')
transRatingWithLabelFile = path.join(path.dirname(argv[0]), r'result/transRatingWithLabelFile.txt')
# user prefer file为存放计算出的用户偏好的文件
userPreferFile = path.join(path.dirname(argv[0]), r'result/userPrefer.txt')

# 用于存放与用户最相似的n个用户的文件
n = 200
listLength = 10  # 推荐列表长度
userSimMatrix = path.join(path.dirname(argv[0]), r'result/userSimMatrix.dict')
CFUUserSimMatrix = path.join(path.dirname(argv[0]), r'result/CFUUserSimMatrix.dict')
combineSimMatrix = path.join(path.dirname(argv[0]), r'result/combineSimMatrix.dict')
recommendDict = path.join(path.dirname(argv[0]), r'result/recommend.dict')
SVDUserSimMatrix = path.join(path.dirname(argv[0]), r'result/SVDUserSim.dict')
userQualityDict = path.join(path.dirname(argv[0]), r'result/userQuality.dict')
userStablityDict = path.join(path.dirname(argv[0]), r'result/userStablityDict.dict')
userFirstRatingDict = path.join(path.dirname(argv[0]), r'result/userFirstRatingDict.dict')
SLOMatrix = path.join(path.dirname(argv[0]), r'result/SLOMatrix.dict')

# 用于存放推荐列表的文件
recommendListFile = path.join(path.dirname(argv[0]), r'result/recommendGradeList.txt')
SLORecommendListFile = path.join(path.dirname(argv[0]), r'result/SLORecommendListFile.txt')

needDivideTrainAndTest = True  # 是否需要划分测试集和训练集
needPreSettle = True  # 是否需要预处理数据
needCFU = False  # 是否需要运行CFU
needTRT = False  # 是否需要进行TRT的运算
needCombine = False  # 是否需要合并CFU和TRT用户矩阵
needUGT = True
needSLO = False
needUPS = False
needEvaluate = True  # 是否需要进行评价


# TRT计算时的time hot算法的参数
G = 1.6  # G为time hot算法的衰减参数,越大衰减越厉害,时间越近的值权重越大
delta = 500  # delta 为移动坐标轴的参数
alpha = 0.1  # 融合用户相似度矩阵时原矩阵分数权重
beta = 0.8
stableTime = 30  # 计算用户偏好稳定性的间隔天数
divideK = 10  # 划分原始数据集为K份
divideMethod = 'random'  # 划分数据集的方式'user','random','time','k'四种

percentage = 0.10  # 运行时每次显示的完成百分比

# label dictionary 为所有电影的类型及其编号
labelDict = {
    'unknown': 0,
    'Action': 1,
    'Adventure': 2,
    'Animation': 3,
    'Children': 4,
    'Comedy': 5,
    'Crime': 6,
    'Documentary': 7,
    'Drama': 8,
    'Fantasy': 9,
    'Film-Noir': 10,
    'Horror': 11,
    'Musical': 12,
    'Mystery': 13,
    'Romance': 14,
    'Sci-Fi': 15,
    'Thriller': 16,
    'War': 17,
    'Western': 18,
    'IMAX': 19,
    '(no genres listed)': 20,
}
labelLength = len(labelDict)

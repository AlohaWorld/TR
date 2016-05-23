import sys
import os
import recsys.algorithm
import recsys.evaluation
import heapq
import cPickle
import stdLib
from recsys.algorithm.factorize import SVD
from recsys.evaluation.decision import PrecisionRecallF1

recsys.algorithm.VERBOSE = True


def load():
    svd.load_data('ratings.txt', sep='::', format={'col': 1, 'row': 0, 'value': 2, 'ids': int})
    [train, test] = svd._data.split_train_test(percent=80.3333103, shuffle_data=False)
    svd.compute(k=4000, min_values=10, pre_normalize=None, mean_center=True, post_normalize=True, savefile='movielens')
    return [train, test]


def toDict(data):
    trdict = {}
    for line in data:
        trdict.setdefault(int(line[1]),{})
        trdict[int(line[1])].setdefault(int(line[2]),0)
        trdict[int(line[1])][(line[2])] = float(line[0])
    return trdict


def usimilarity(data):
    simMatrix = dict()
    PROCESS = len(data)
    cnt = 0.0
    for i in data.keys():
        cnt+=1
        for j in data.keys():
            if i == j:
                continue
            sim = float(svd.similarity(i,j))
            #print 'i: %s, j: %s, sim: %f' % (i,j,sim)
            if sim > 0:
                simMatrix.setdefault(i,list())
                simMatrix[i].append((j,sim))
        if i in simMatrix:
            simMatrix[i] = heapq.nlargest(200,simMatrix[i], key=lambda x: x[1])
        if cnt % int(PROCESS * 0.10) == 0:
                print '\r%.1f%%' % (100 * cnt / PROCESS)
    filename = "svdUserSimMatrix.dict"
    stdLib.dumpData(simMatrix,filename)


def recommend(data):
    fw = open('recList.txt','w')
    for user in data.keys():
        reclist = {}
        reclist.setdefault(user,[])
        itemList = svd.recommend(user,n=50)
        reclist[user]=itemList
        fw.write(str(reclist)+'\n')
    fw.close()


def evaluation(data):
    resData = {}
    res = open('recList.txt','r').readlines()
    for l in res:
        tmp = eval(l)
        uid = int(tmp.keys()[0])
        resData.setdefault(uid,{})
        for item in tmp[uid]:
            mid = int(item[0])
            rating = float(item[1])
            resData[uid].setdefault(mid,0)
            resData[uid][mid] = rating
    hit = 0
    recall = 0
    precision = 0
    for uid in resData.keys():
        tu = data.get(uid,{})
        for mid in resData[uid]:
            if mid in tu:
                hit+=1
        #print hit
        recall += len(tu)
        precision+=50
    recall = hit * 100 / (recall * 1.0)
    precision = hit * 100 / (precision * 1.0)
    if recall != 0 and precision != 0:
        return [recall, precision]
    else:
        return [0, 0]

def fvalue(rap):
    if rap[0] == 0 and rap[1] == 0:
        return 0
    return rap[0] * rap[1] * 2 / (rap[0] + rap[1])


if __name__=='__main__':
    svd = SVD()
    train = []
    test = []
    [train,test] = load()
    uidict =  toDict(train)
    tedict = toDict(test)
    usimilarity(uidict)
    recommend(uidict)
    rap = evaluation(tedict)
    print rap
    f = fvalue(rap)
    print f
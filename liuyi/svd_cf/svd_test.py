import sys
import os
import recsys.algorithm
import recsys.evaluation
from recsys.algorithm.factorize import SVD
from recsys.evaluation.decision import PrecisionRecallF1

recsys.algorithm.VERBOSE = True

def load():
    svd.load_data('ratings.txt', sep='::', format={'col': 0, 'row': 1, 'value': 2, 'ids': int})
    svd.compute(k=100, min_values=10, pre_normalize=None, mean_center=True, post_normalize=True, savefile='movielens')


def split(train, test):
    [train, test] = svd._data.split_train_test(shuffle_data=False)
    return [train, test]

def toDict(data):
    trdict = {}
    for line in data:
        trdict.setdefault(int(line[2]),{})
        trdict[int(line[2])].setdefault(int(line[1]),0)
        trdict[int(line[2])][(line[1])] = float(line[0])
    return trdict


def recommend(data):
    fw = open('recList.txt','a')
    for user in data.keys():
        reclist = {}
        reclist.setdefault(user,[])
        itemList = svd.recommend(user,n=50,is_row=False)
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
        precision+=20
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
    load()
    train = []
    test = []
    [train,test] = split(train,test)
    uidict =  toDict(train)
    tedict = toDict(test)
    recommend(uidict)
    rap = evaluation(tedict)
    print rap
    f = fvalue(rap)
    print f
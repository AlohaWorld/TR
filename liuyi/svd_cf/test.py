import os
import sys



resData = {}
res = open('recList.txt','r').readlines()
for l in res:
    tmp = eval(l)
    uid = int(tmp.keys()[0])
    resData.setdefault(uid,{})
    for item in tmp[uid]:
        mid = item[0]
        rating = item[1]
        resData[uid].setdefault(mid,0)
        resData[uid][mid] = rating
#print resData
tu = resData.get(3921,{})
print tu
if 2019 in tu:
    print 1
else:
    print 0
'''
hit = 0
precision = 0
recall = 0
for uid in resData.keys():
    tu = data.get(uid,{})
    for mid in resData[uid]:
        if mid in tu:
            hit+=1
    recall += len(tu)
    precision+=20
recall = hit * 100 / (recall * 1.0)
precision = hit * 100 / (precision * 1.0)
'''
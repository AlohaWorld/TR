# -*- coding:utf-8 -*-

import cPickle
import os
from os import path
from sys import argv

def writeOpen(fileID, para):
    fileID = path.join(path.dirname(argv[0]), fileID)
    if os.path.exists(fileID):
        print fileID + '...existed!'
        os.remove(fileID)
        print fileID + '...deleted!'    
    fout = open(fileID, para)
    print fileID + '...created!'
    return fout

def dumpData(data, fin):
    w = writeOpen(fin, 'wb')
    cPickle.dump(data, w)
    w.close()

def loadData(pickleFile):
    '''
    read the pickle file to parameter
    :param dictionaryFile: data type: pickle file    
    return type: dict
    '''
    r = open(pickleFile, 'rb')
    data = cPickle.load(r)    
    r.close()    
    return data

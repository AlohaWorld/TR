#!/env/python
# -*- encoding: utf-8 -*-

"""
@version: 0.1
@author: wenzhiquan
@contact: wenzhiquanr@163.com
@site: http://github.wenzhiquan.com
@software: PyCharm
@file: transRating.py
@time: 16/5/25 下午2:55
@description: null
"""
from TRT.config import config

def transRating():
    filename = config.ratingWithLabelFile
    read = open(filename)
    data = read.readlines()
    read.close()
    result = list()

    for line in data:
        tmp = line[:-1].split(config.separator)
        tmp[2] = str(float(tmp[2]) - 3)
        result.append(config.separator.join(tmp) + "\n")

    outfile = config.transRatingWithLabelFile
    out = open(outfile, 'w')
    for i in result:
        out.write(i)
    out.close()
import sys
import os

ftr = open("trainRatings.txt","r")
fw = open("ratings.txt","a")
for line in ftr.readlines():
    fw.write(line)
ftr.close()
fte = open("testRatings.txt","r")
for line in fte.readlines():
    fw.write(line)
fte.close()
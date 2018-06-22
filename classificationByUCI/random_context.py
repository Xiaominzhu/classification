# -*- coding:utf-8-*-
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def context(writePath):
    fwrite = open(writePath, "w+")
    for i in range(rows):
        nums = 0
        for j in range(cows):
            randomVal = random.uniform(0, 1)
            if(randomVal >= 0.3):
                fwrite.write(str(nums) + " ")
            nums += 1
        fwrite.write("\n")

def combine(writePath, combinepath, cows):
    f = open(writePath, 'r')
    fwrite = open(combinepath, "w+")
    attriindx = [i for i in range(cows)]
    for line in f.readlines():
        fwrite.write(line.strip("\r\n"))
        lineList = line.strip(" \r\n").split(" ")
        for i in attriindx:
            if str(i) not in lineList:
                fwrite.write(str(i + cows) + " ")
        fwrite.write("\n")


if __name__ == '__main__':
    rootpath = "F:/englisgpaper2/"
    rows = 90
    cows = 10
    writePath = rootpath + "context_" + str(rows) + "_" + str(cows) + ".txt"
    combinepath = rootpath + "context_" + str(rows) + "_" + str(cows) \
                  + "_com" + ".txt"
    context(writePath)
    combine(writePath,combinepath, cows)
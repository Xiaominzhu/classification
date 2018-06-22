# -*- coding:utf-8-*-
from __future__ import division
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def caluleAver(path):
    f = open(path, 'r')
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
    lineNums = 0
    for line in f.readlines():
        lineNums += 1
        linelist = line.strip("\r\n").split(",")
        sum1 += float(linelist[0])
        sum2 += float(linelist[1])
        sum3 += float(linelist[2])
        sum4 += float(linelist[3])
    averList = [sum1/lineNums, sum2/lineNums, sum3/lineNums, sum4/lineNums]
    return averList

#数据集预处理
def createContext(averList, path, Datapath):
    print averList
    attriList = averList +\
               ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]  # 4,5,6
    f = open(path, 'r')
    fwrite = open(Datapath, 'w+')
    for line in f.readlines():
        linelist = line.strip("\r\n").split(",")
        for i in range(len(linelist) - 1):
            if(float(linelist[i]) >= float(attriList[i])):
                fwrite.write(str(i) + " ")
        fwrite.write(str(attriList.index(linelist[-1])))
        fwrite.write(" \n")
        fwrite.flush()

#将数据集划分为 训练集：测试集 = 0.8：0.2
def divideData(Datapath, trainPath, testPath):
    f = open(Datapath, "r")
    fwriteTest = open(testPath, "w+")
    fwriteTrain = open(trainPath, "w+")
    for line in f.readlines():
        randomvalue = random.uniform(0, 1)
        if (randomvalue <= 0.8):
            fwriteTrain.write(line)
        else:
            fwriteTest.write(line)

def combineContext(trainPath, combinepath, atrributeNum):
    f = open(trainPath, 'r')
    fwrite = open(combinepath, "w+")
    attriindx = [i for i in range(atrributeNum)]
    for line in f.readlines():
        fwrite.write(line.strip("\r\n"))
        lineList = line.strip(" \r\n").split(" ")
        for i in attriindx:
            if str(i) not in lineList:
                fwrite.write(str(i + atrributeNum) + " ")
        fwrite.write("\n")

def contextTr(contextpath, contextTrPath, atrributeNum):
    f = open(contextpath, 'r')
    fwrite = open(contextTrPath, 'w+')
    objAttrDic = {}
    objNums = 0
    for line in f.readlines():
        objAttrDic[str(objNums)] = line.strip(" \r\n").split(" ")
        objNums += 1
    for i in range(atrributeNum):
        for items in objAttrDic.items():
            if(str(i) in items[1]):
                fwrite.write(items[0] + " ")
        fwrite.write("\n")

if __name__ == '__main__':
    rootpath = "F:/englisgpaper2/Iris/"
    path = rootpath + "irisData.txt"
    averList = caluleAver(path)
    Datapath = rootpath + "Data.txt"
    createContext(averList, path, Datapath)

    trainPath = rootpath + "trainData.txt"
    testPath = rootpath + "testData.txt"
    validationPath = rootpath + "validationData.txt"
    divideData(Datapath, trainPath, testPath)

    combinepath = rootpath + "CombineContext.txt"
    atrributeNum = 7
    combineContext(trainPath, combinepath, atrributeNum)
    contextTrPath = rootpath + "ContextTr.txt"
    contextTr(trainPath, contextTrPath, atrributeNum)








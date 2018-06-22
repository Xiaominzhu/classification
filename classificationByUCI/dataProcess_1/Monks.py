# -*- coding:utf-8-*-
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#数据集预处理
def createContext(path, Datapath):
    attri= [['0', '1'],
              ['1', '2', '3'],
              ['1', '2', '3'],
              ['1', '2'],
              ['1', '2', '3'],
              ['1', '2', '3', '4'],
              ['1', '2']]
    leng = len(attri)
    f = open(path, 'r')
    fwrite = open(Datapath, 'w+')
    for line in f.readlines():
        linelist = line.strip("\n").split(" ")[1:-1]
        for j in range(leng):
            elem = linelist[j]
            valueSum = 0
            if(j > 0):
                valueSum = 0
                for i in range(j):
                    valueSum = valueSum + len(attri[i])
            indx = attri[j].index(elem) + valueSum
            fwrite.write(str(indx) + " ")
        fwrite.write("\n")
    print "sttrinums: ", sum([len(k) for k in attri])
    return sum([len(k) for k in attri])

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
    rootpath = "F:/englisgpaper2/monks/"
    pathTrain = rootpath + "monks-1-train.txt"
    pathTrain_context = rootpath + "contextTrain.txt"
    atrributeNum = createContext(pathTrain, pathTrain_context)

    pathTest = rootpath + "monks-1-test.txt"
    pathTest_context = rootpath + "contextTest.txt"
    createContext(pathTest, pathTest_context)

    combinepath = rootpath + "CombineContext.txt"
    combineContext(pathTrain_context, combinepath, atrributeNum)
    contextTrPath = rootpath + "ContextTr.txt"
    contextTr(pathTrain_context, contextTrPath, atrributeNum)








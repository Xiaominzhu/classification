# -*- coding:utf-8-*-
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#数据集预处理
def createContext(path, Datapath):
    attri= [['usual','pretentious','great_pret'],
              ['proper', 'less_proper', 'improper', 'critical', 'very_crit'],
              ['complete', 'completed', 'incomplete', 'foster'],
              ['1', '2', '3', 'more'],
              ['convenient', 'less_conv', 'critical'],
              ['convenient', 'inconv'],
              ['nonprob', 'slightly_prob', 'problematic'],
              ['recommended', 'priority', 'not_recom'],
              ['not_recom', 'very_recom', 'priority', 'spec_prior']]
    # 27,28,29,30
    leng = len(attri)
    f = open(path, 'r')
    fwrite = open(Datapath, 'w+')
    for line in f.readlines():
        if(random.uniform(0,1)>0.98):
            linelist = line.strip("\r\n").split(",")
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

#将数据集划分为 训练集：测试集：验证集 = 0.6：0.2：0.2
def divideData(Datapath, trainPath, testPath, validationPath):
    f = open(Datapath, "r")
    fwriteTest = open(testPath, "w+")
    fwriteVali = open(validationPath, "w+")
    fwriteTrain = open(trainPath, "w+")
    for line in f.readlines():
        randomvalue = random.uniform(0, 1)
        if (randomvalue <= 0.6):
            fwriteTrain.write(line)
        if(randomvalue > 0.6 and randomvalue <= 0.8):
            fwriteTest.write(line)
        if(randomvalue>0.8):
            fwriteVali.write(line)

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
    path = "F:/englisgpaper2/UCI2/NurseryData.txt"
    Datapath = "F:/englisgpaper2/UCI2/Data.txt"
    createContext(path, Datapath)
    trainPath = "F:/englisgpaper2/UCI2/trainData.txt"
    testPath = "F:/englisgpaper2/UCI2/testData.txt"
    validationPath = "F:/englisgpaper2/UCI2/validationData.txt"
    divideData(Datapath, trainPath, testPath, validationPath)

    combinepath = "F:/englisgpaper2/UCI2/CombineContext.txt"
    atrributeNum = 31
    combineContext(trainPath, combinepath, atrributeNum)
    contextTrPath = "F:/englisgpaper2/UCI2/ContextTr.txt"
    contextTr(trainPath, contextTrPath, atrributeNum)








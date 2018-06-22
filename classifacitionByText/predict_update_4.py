# -*- coding:utf-8-*-
from __future__ import division
from classifiByThreeConcepts import JieBaContext_1
from pylab import *
import os
import jieba
jieba.load_userdict("F:/graduationThesis/dataSet/test/addDict.txt")
from classifiByTwoConcepts import predict_4
from classifiByThreeConcepts import ProcessTest
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def tesData():
    rootpath = "F:/graduationThesis/dataSet/test/classifiByThreeConcepts/"
    path = rootpath + "traindata1/"
    namelist = os.listdir(path)
    testpath = rootpath + "testdata/"
    for f in os.listdir(testpath):
        os.remove(testpath + f)
    for i in range(0, 10, 1):
        for n in namelist:
            testNums = 0
            textname = os.path.splitext(n)[0]
            if(textname.find("_") == -1):
                testWrite = open(testpath + textname + str(i) + ".txt", "w+")
                fread = open(path + n, 'r')
                lines = fread.readlines()
                if(len(lines)>350):
                    for k in range(len(lines)-i*35-1, 0, -1):
                        testNums += 1
                        testWrite.write(lines[k])
                        if(testNums > 35):
                            break
                else:
                    for k in range(len(lines)-i*10-1, 0, -1):
                        testNums += 1
                        testWrite.write(lines[k])
                        if(testNums > 35):
                            break
def jieba():
    rootpath = "F:/graduationThesis/dataSet/test/classifiByThreeConcepts/"
    path = rootpath + "testdata/"
    namelist = os.listdir(path)
    for n in namelist:
        textname = os.path.splitext(n)[0]
        testdataPath = path + n
        jiebaPath = path + textname + "_jieba.txt"
        predict_4.tesjieba(testdataPath, jiebaPath)

def feature(allwords):
    rootpath = "F:/graduationThesis/dataSet/test/classifiByThreeConcepts/"
    path = rootpath + "testdata/"
    namelist = os.listdir(path)
    for n in namelist:
        textname = os.path.splitext(n)[0]
        if(textname.find("_jieba") != -1):
            jiebaPath = path + n
            featurePath = path + textname + "_feature.txt"
            predict_4.getPresent(allwords, jiebaPath, featurePath)
    namelist2 = os.listdir(path)
    for i in range(0, 10, 1):
        for m in namelist2:
            textname2 = os.path.splitext(m)[0]
            if (textname2.find(str(i) + "_jieba_feature") != -1):
                writePath = path + "feature_" + str(i) + ".txt"
                fwrite = open(writePath, "a+")
                for line in open(path + m, 'r'):
                    fwrite.write(line)

def predict(labelindex):
    rootpath = "F:/graduationThesis/dataSet/test/classifiByThreeConcepts/"
    path = rootpath + "testdata/"
    namelist = os.listdir(path)
    precisionThree = []
    precisionTwo = []
    interP_three, interN_three, suppP_three, suppN_three = 0.6, 0.5, 0.3, 0.2
    interP_two, suppP_two = 0.2, 0.7
    for i in range(0, 10, 1):
        for n in namelist:
            textname = os.path.splitext(n)[0]
            if(textname.find("feature_") != -1):

                valueThree = ProcessTest.Predict(path + n, interP_three, interN_three,
                                                 suppP_three, suppN_three, labelindex)
                precisionThree.append(valueThree)
                valueTwo = predict_4.Predict(path + n, interP_two, suppP_two, labelindex)
                precisionTwo.append(valueTwo)
    return precisionThree, precisionTwo

if __name__ == '__main__':
    newsSelectNums = 75
    classNums = 26
    rootpath = "F:/graduationThesis/dataSet/test/classifiByThreeConcepts/"

    writePath = rootpath + "traindata_" + str(newsSelectNums) + ".txt"
    JiebaPath = rootpath + "traindata_" + str(newsSelectNums) + "_Jieba.txt"
    JieBaContext_1.jiebase(writePath, JiebaPath)

    wordsList, labelList = JieBaContext_1.labelwordsList(JiebaPath)
    allwords = wordsList + labelList
    print "len(allwords): ", len(allwords)
    labelindex = []
    for key in labelList:
        labelindex.append(str(allwords.index(key)))
    wordsindex = []
    for key in wordsList:
        wordsindex.append(str(allwords.index(key)))

    tesData()
    jieba()
    feature(allwords)
    precisionThree, precisionTwo = predict(labelindex)
    print "precisionThree: ", precisionThree
    print "precisionTwo: ", precisionTwo
    # figure(precisionThree, precisionTwo)
    # figure()
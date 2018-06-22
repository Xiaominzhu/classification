# -*- coding:utf-8-*-
from __future__ import division
from sklearn import tree
import numpy

def trainData(trainPath):
    f = open(trainPath, 'r')
    train_X = []
    train_Y = []
    for line in f.readlines():
        lineList = line.strip(" \r\n").split(" ")
        train_X.append(lineList[:-1])
        train_Y.append(lineList[-1])
    return numpy.array(train_X), numpy.array(train_Y)

def teetData(testPath):
    f = open(testPath, 'r')
    test_X = []
    test_Y = []
    for line in f.readlines():
        lineList = line.strip(" \r\n").split(" ")
        test_X.append(lineList[:-1])
        test_Y.append(lineList[-1])
    return numpy.array(test_X), numpy.array(test_Y)

def decisionTree_(train_X, train_Y, test_X, test_Y):
    clf = tree.DecisionTreeClassifier(criterion = 'entropy')
    clf.fit(train_X, train_Y)

    predict_Y = clf.predict(test_X)
    correct = 0
    for i in range(len(predict_Y)):
        if(predict_Y[i] == test_Y[i]):
            correct += 1
    print correct/len(predict_Y)

if __name__ == "__main__":
    rootpath = "F:/englisgpaper2/UCI2/"
    trainPath = rootpath + "trainData.txt"
    trainData(trainPath)
    testPath = rootpath + "testData.txt"
    teetData(testPath)
    train_X, train_Y = trainData(trainPath)
    test_X, test_Y = teetData(testPath)
    decisionTree_(train_X, train_Y, test_X, test_Y)








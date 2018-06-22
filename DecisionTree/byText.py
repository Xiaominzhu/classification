# -*- coding:utf-8-*-
from __future__ import division
from classifiByThreeConcepts import JieBaContext_1
from sklearn import tree
import numpy
from sklearn.grid_search import GridSearchCV

usenature = ("Ag","ad","an","b","dg","g","h","i",
          "j","k","l","Ng","n","nr","ns","nt","nz",
          "s","tg","t","vg","v","vd","vn","x","z",
          "un")

def trainData(wordsindex, labelindex):
    path = "F://graduationThesis//dataSet//test//" \
           "classifiByThreeConcepts//reducedContext.txt"
    f = open(path, 'r')
    train_X = []
    train_Y = []
    for line in f.readlines():
        lineList = line.strip("\r\n").split(" ")
        tmp_X = []
        for i in wordsindex:
            if(i in lineList):
                tmp_X.append(1)
            else:
                tmp_X.append(0)
        train_X.append(tmp_X)
        for j in labelindex:
            if(j in lineList):
                train_Y.append(labelindex.index(j))
    return numpy.array(train_X), numpy.array(train_Y)

def teetData(wordsindex, labelindex):
     Path = 'F:/graduationThesis/dataSet/test/classifiByThreeConcepts/featurePresent.txt'
     f = open(Path, 'r')
     test_X = []
     test_Y = []
     for line in f.readlines():
         lineList = line.strip("\r\n").split(":")[1].split(" ")
         label = line.strip("\r\n").split(":")[0].split(" ")
         tmp_X = []
         for i in wordsindex:
             if (i in lineList):
                 tmp_X.append(1)
             else:
                 tmp_X.append(0)
         test_X.append(tmp_X)
         for j in labelindex:
             if (j in label):
                 test_Y.append(labelindex.index(j))
     return numpy.array(test_X), numpy.array(test_Y)


if __name__ == "__main__":
    wordsList, labelList = JieBaContext_1.labelwordsList()
    allwords = wordsList + labelList

    labelindex = []
    for key in labelList:                                       # label在allwords中对应的索引
        labelindex.append(str(allwords.index(key)))
    print "labelindex: ", labelindex
    wordsindex = []
    for key in wordsList:
        wordsindex.append(str(allwords.index(key)))
    allwordsindex = wordsindex + labelindex
    train_X, train_Y = trainData(wordsindex, labelindex)
    test_X, test_Y = teetData(wordsindex, labelindex)
    # for depth in range(4,10):
    #     for leaf in range(2,10):
    #         for split_ in range(2, 10):
    #             clf = tree.DecisionTreeClassifier(criterion='gini', splitter='best',
    #                                               max_depth = depth, min_samples_leaf = leaf,
    #                                               min_samples_split = split_)
    clf = tree.DecisionTreeClassifier()
    clf.fit(train_X, train_Y)
    predict_Y = clf.predict(test_X)
    correct = 0
    for i in range(len(predict_Y)):
        if(predict_Y[i] == test_Y[i]):
            correct += 1
    print correct/len(predict_Y)







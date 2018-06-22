# -*- coding:utf-8-*-
from __future__ import division
from pylab import *
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def predict(testpath, test_predict, rulespath):
    interP, interN, suppP, suppN = 0.5, 0.5, 0.3, 0.3
    namelist = os.listdir(rulespath)
    lineNums = 0
    correctNums = 0
    accuracymax = 0

    f = open(testpath, 'r')
    fwrite = open(test_predict, 'w+')
    for line_test in f.readlines():
        lineNums += 1
        if(lineNums>1):
            break
        labeldic = {}
        linelist = line_test.strip(" \r\n").split(" ")
        feature = linelist[0:-1]
        actual = linelist[-1]
        for fil in namelist:
            print "fil: ", fil
            WSval = 0
            readpath = rulespath + fil
            label = os.path.splitext(fil)[0].split("_")[1]
            fread = open(readpath, 'r')
            for line in fread.readlines():
                lineList = line.strip(" \r\n").split(",")
                ruletype = lineList[0].split("|")[0]
                rules = lineList[2].split(" --")
                antecedent = rules[0].split(" ")
                supp = lineList[0].split(":")[1]
                # conf = lineList[1].split(":")[1]

                # 分类规则前件与特征的交集个数
                interNums = len(set(feature).intersection(set(antecedent)))
                if (interNums > 0):
                    print "rule: ", line.strip("\r\n")
                    print "interSet: ", set(feature).intersection(set(antecedent))
                    if (ruletype == "PP"):
                        WSval = WSval + suppP * float(supp)+ \
                                interP * interNums / len(set(antecedent))
                    if (ruletype == "PN"):
                        WSval = WSval - suppN * float(supp) \
                                - interN * interNums / len(set(antecedent))
                    print "WSval: ", WSval
                    print "\n"
            print "*********************************"
            labeldic[label] = WSval
        labeldic_Sort = sorted(labeldic.items(), key=lambda item: item[1],
                                    reverse = True)
        predict_value = labeldic_Sort[0][0]
        print "labeldic_Sort: ", labeldic_Sort
        print "predict_value: ", predict_value
        print "actual: ", actual
        print "********************************"
        fwrite.write(line_test.strip(" \r\n") + " " + predict_value + "\n")
        if(predict_value == actual):
            correctNums += 1
    accuracy = correctNums/lineNums
    if(accuracy >= accuracymax):
        accuracymax = accuracy
        interPbest = interP
        interNbest = interN
        suppPbest = suppP
        suppNbest = suppN
        print accuracymax, interPbest, interNbest, suppPbest, suppNbest
if __name__ == '__main__':
    rootpath = "F:/englisgpaper2/UCI2/"
    testpath = rootpath + "testData.txt"
    test_predict = rootpath + "testPredict.txt"
    rulespath = rootpath + "rules_tmp3/"
    predict(testpath, test_predict, rulespath)

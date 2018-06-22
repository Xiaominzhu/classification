# -*- coding:utf-8-*-
from __future__ import division
from pylab import *
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
minsupp = 0.1
minconf = 0.5

def filter_(rulespath, filterPath):
    # 删除原来存在的文本文件
    for f in os.listdir(filterPath):
        os.remove(filterPath + f)
    namelist = os.listdir(rulespath)
    for f in namelist:
        print "f: ", f
        fread = open(rulespath + f, 'r')
        for line in fread.readlines():
            lineList = line.strip(" \r\n").split(",")
            supp = float(lineList[0].split(":")[1])
            conf = float(lineList[1].split(": ")[1])
            if(supp >= minsupp and conf >= minconf):
                fwrite = open(filterPath + f, "a+")
                fwrite.write(line)

def selectRules(line_test, rulespath, rulesSelect):
    # 删除原来存在的文本文件
    for f in os.listdir(rulesSelect):
        os.remove(rulesSelect + f)
    namelist = os.listdir(rulespath)
    linelist = line_test.strip(" \r\n").split(" ")
    feature = linelist[0:-1]
    for fil in namelist:
        readpath = rulespath + fil
        label = os.path.splitext(fil)[0].split("_")[1]
        fread = open(readpath, 'r')
        for line in fread.readlines():
            lineList = line.strip(" \r\n").split(",")
            ruletype = lineList[0].split("|")[0]
            rules = lineList[2].split(" --")
            antecedent = rules[0].split(" ")

            # 分类规则前件与特征的交集个数
            interNums = len(set(feature).intersection(set(antecedent)))
            if (interNums > 0):
                if (ruletype == "PP"):
                    fwrite1 = open(rulesSelect + "labelPP_" + label + ".txt", "a+")
                    fwrite1.write(line)
                if (ruletype == "PN"):
                    fwrite2 = open(rulesSelect + "labelPN_" + label + ".txt", "a+")
                    fwrite2.write(line)

# 利用插入排序，依次针对置信度、支持度进行排序
def sort_elem(strList):
    sortList = []
    sortList.append(strList[0])
    strList = strList[1:]
    leng = len(strList)
    for i in range(leng):
        sortLen = len(sortList)
        movestep = 0
        supp = float(strList[i].strip(" \n").split(",")[0].split(":")[1])
        conf = float(strList[i].strip(" \n").split(",")[1].split(":")[1])
        for j in range(sortLen-1, -1, -1):
            supp_ori = float(sortList[j].strip(" \n").split(",")[0].split(":")[1])
            conf_ori = float(sortList[j].strip(" \n").split(",")[1].split(":")[1])
            if((conf > conf_ori) or (conf == conf_ori and supp > supp_ori)):
                movestep += 1
            else:
                break
        sortList.insert(sortLen - movestep, strList[i])
    return sortList

def remainfive(rulesSelect):
    namelist = os.listdir(rulesSelect)
    labelrulesDic = {}
    for fil in namelist:
        label = os.path.splitext(fil)[0].split("_")[1]
        readpath = rulesSelect + fil
        lines = open(readpath, 'r').readlines()
        original = lines[0:10]
        sortList = sort_elem(original)
        sortLen = len(sortList)

        for i in range(sortLen, len(lines)):
            movestep = 0
            supp = lines[i].strip(" \r\n").split(",")[0].split(":")[1]
            conf = lines[i].strip(" \r\n").split(",")[1].split(":")[1]
            for j in range(sortLen - 1, -1, -1):
                supp_ori = sortList[j].strip(" \n").split(",")[0].split(":")[1]
                conf_ori = sortList[j].strip(" \n").split(",")[1].split(":")[1]
                if((conf > conf_ori) or (conf == conf_ori and supp > supp_ori)):
                    movestep += 1
                else:
                    break
            sortList.insert(sortLen - movestep, lines[i])
            sortList.remove(sortList[-1])
        # print "sortList: ", sortList
        if(label not in labelrulesDic.keys()):
            labelrulesDic[label] = sortList
        else:
            originalelem = labelrulesDic[label]
            labelrulesDic[label] = originalelem + sortList
    return labelrulesDic

def predict(testpath, test_predict, rulespath, rulesSelect):
    interP, interN, suppP, suppN = 0.6, 0.5, 0.3, 0.2
    lineNums = 0
    correctNums = 0
    f = open(testpath, 'r')
    fwrite = open(test_predict, 'a+')
    for line_test in f.readlines():
        # print "line_test: ", line_test
        feature = line_test.strip(" \r\n").split(" ")[0:-1]
        actual = line_test.strip(" \r\n").split(" ")[-1]

        # 分别找出各个类别与之相关的5个规则
        lineNums += 1
        if(lineNums % 100 == 0):
            print lineNums
        labeldic = {}
        selectRules(line_test, rulespath, rulesSelect)
        labelrulesDic = remainfive(rulesSelect)
        labelrules_len = len(labelrulesDic)
        # print "labelrulesDic: ", labelrulesDic
        # print "labelrules_len: ", labelrules_len
        for items in labelrulesDic.items():
            # print "items: ", items
            label = items[0]
            ruleList = items[1]
            WSval = 0

            # 利用找出的规则进行预测
            for ruleelem in ruleList:
                list1 = ruleelem.strip(" \r\n").split(",")
                ruletype = list1[0].split("|")[0]
                supp = list1[0].split(":")[1]
                rules = list1[2].split(" --")
                antecedent = rules[0].split(" ")

                # 分类规则前件与特征的交集个数
                interNums = len(set(feature).intersection(set(antecedent)))

                # print "interSet: ", set(feature).intersection(set(antecedent))
                if (ruletype == "PP"):
                    WSval = WSval + suppP * float(supp) + \
                            interP * interNums / len(set(antecedent))
                if (ruletype == "PN"):
                    WSval = WSval - suppN * float(supp) \
                            - interN * interNums / len(set(antecedent))
            labeldic[label] = WSval
        labeldic_Sort = sorted(labeldic.items(), key=lambda item: item[1],
                           reverse=True)
        # print "labeldic_Sort: ", labeldic_Sort
        predict_value = labeldic_Sort[0][0]
        # print "labeldic_Sort: ", labeldic_Sort
        # print "predict_value: ", predict_value
        # print "actual: ", actual
        # print "********************************"
        fwrite.write(line_test.strip(" \r\n") + " " + predict_value + "\n")
        fwrite.flush()
        if (predict_value == actual):
            correctNums += 1
    accuracy = correctNums / lineNums
    print accuracy

if __name__ == '__main__':
    rootpath = "F:/englisgpaper2/UCI/"
    testpath = rootpath + "testData.txt"
    test_predict = rootpath + "testPredict.txt"
    rulespath = rootpath + "rules_tmp3/"
    filterPath = rootpath + "rules_tmp4/"
    filter_(rulespath, filterPath)
    rulesSelect = rootpath + "rules_select/"
    predict(testpath, test_predict, filterPath, rulesSelect)

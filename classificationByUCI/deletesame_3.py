# -*- coding:utf-8-*-
from __future__ import division
import os

# 不同类别的分类规则写在不同的文件中,再此之前删除原来存在的文件
def labelfile(rulesPath, tmp1path):
    frules = open(rulesPath, 'r')
    for f in os.listdir(tmp1path):
        os.remove(tmp1path + f)
    nums = 0
    for line in frules.readlines():
        if(nums % 1000 == 0):
            print nums
        nums += 1
        lineList = line.strip(" \r\n").split(",")
        labelList = lineList[2].split(" --")[1].split(" ")
        print "labelList: ", labelList
        for label in labelList:
            fwrite = open(tmp1path + "label_" + label + ".txt", "a+")
            # if(label in antecedentList):
            #     antecedentStr = "".join([j for j in antecedentList
            #                              if j not in labelindex])
            #     fwrite.write(line.strip(" \r\n").split(",")[0] + ","
            #                  + antecedentStr + " --" + label)
            # else:
            fwrite.write(line)

# 针对每个文件去重,首先列 行去重
def removeSame1(tmp1path, tmp2path):
    for ff in os.listdir(tmp2path):
        os.remove(tmp2path + ff)
    for f in os.listdir(tmp1path):
        nums = 0
        flag = 0
        frontflag = ""
        middleflag = set([])
        behindflag = set([])
        for line in open(tmp1path + f, 'r').readlines():
            if(nums % 1000 == 0):
                print nums
            nums += 1
            lineList = line.strip(" \r\n").split(",")
            frontStr = lineList[0]
            middleSet = set(lineList[2].split(" --")[0].split(" "))
            behindSet = set(lineList[2].split(" --")[1].split(" "))
            if(flag == 0):
                fwrite = open(tmp2path + f, "a+")
                fwrite.write(line)
                flag += 1
                frontflag = frontStr
                middleflag = middleSet
                behindflag = behindSet
            else:
                if((frontStr != frontflag) or (middleSet != middleflag)
                   or (behindSet != behindflag)):
                    fwrite = open(tmp2path + f, "a+")
                    fwrite.write(line)
                    frontflag = frontStr
                    middleflag = middleSet
                    behindflag = behindSet

def removeSame2(tmp2path, path):
    nums = 0
    for ff in os.listdir(path):
        os.remove(path + ff)
    for f in os.listdir(tmp2path):
        print f
        ruleList = []
        for line in open(tmp2path + f, 'r').readlines():
            if(nums % 1000 == 0):
                print nums
            nums += 1
            lineStr = line.strip(" \r\n")
            if(lineStr not in set(ruleList)):
                ruleList.append(lineStr)
                fwrite = open(path + f, "a+")
                fwrite.write(line)

if __name__ == "__main__":
    rootpath = "F:/englisgpaper2/Iris/"
    rulesPath = rootpath + "rules.txt"
    tmp1path = rootpath + "rules_tmp1/"
    labelfile(rulesPath, tmp1path)

    tmp2path = rootpath + "rules_tmp2/"
    path = rootpath + "rules_tmp3/"
    removeSame1(tmp1path, tmp2path)
    removeSame2(tmp2path, path)


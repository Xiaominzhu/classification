# -*- coding:utf-8-*-

from __future__ import division
minsupPP = 0.01
minsupPN = 0.01
minconfiPP = 0.5
minconfiPN = 0.5


# 构建字典，表示属性被那些对象拥有
def attrobjectDic(contextTrpath):
    f = open(contextTrpath, 'r')
    attrobjectdic = {}
    nums = 0
    for line in f.readlines():
        attrobjectdic[str(nums)] = set(line.strip(" \r\n").split(" "))
        nums += 1
    return attrobjectdic

#构建字典，表示属性不被那些对象拥有
def attrnotobjectDic(objNums,contextTrpath):
    f = open(contextTrpath, 'r')
    attrnotobjectdic = {}
    indexList = [str(i) for i in range(objNums)]
    nums = 0
    for line in f.readlines():
        listtmp = []
        lineList = line.strip(" \r\n").split(" ")
        for v in indexList:
            if(v not in lineList):
                listtmp.append(v)
        attrnotobjectdic[str(nums)] = set(listtmp)
        nums += 1
    return attrnotobjectdic

# 根据fcbo算法计算三支概念（已经正负属性）
def threeRules_fcbo(attrNums, outPath, rulesPath, newsNums,
           attrobjectdic, attrnotobjectdic, labelindex):
    fwrite = open(rulesPath, 'w+')
    nums = 0
    A1C1Combine = []
    A1C2Combine = []
    newsNumsList = [str(k) for k in range(newsNums)]
    with open(outPath, 'r') as f:
        for elem in f:
            nums += 1
            if(len(A1C1Combine) > 5000):
                A1C1Combine = []
            if(len(A1C2Combine) > 5000):
                A1C2Combine = []
            if(nums % 10000 == 0):
                # A1C1Combine = []
                # A1C2Combine = []
                print nums
                # print A1C1Combine
                # print A1C2Combine
                print len(A1C1Combine), len(A1C2Combine)
                # print "*********"
            attrList = elem.strip(" \r\n").split(" ")
            posAttr = set([i for i in attrList if int(i) < attrNums])
            negAttr = set([str(int(j)-attrNums) for j in attrList if int(j) >= attrNums])

            # 判断共同具有正属性的文档相关参数值,每个三支概念形式为(X,(A1C1,A2C2))
            if(posAttr not in A1C1Combine):
                A1C1Combine.append(posAttr)
                C1 = set([i for i in posAttr if i in labelindex])
                A1 = set([i for i in posAttr if i not in labelindex])
                C1Inter = set(newsNumsList)
                A1Inter = set(newsNumsList)
                if (C1 == set([])):
                    C1Inter = set()
                if (C1 != set([])):
                    for val in tuple(C1):
                        C1Inter = C1Inter & attrobjectdic[val]
                if (A1 == set([])):
                    continue
                for val in tuple(A1):
                    A1Inter = A1Inter & attrobjectdic[val]
                newsNumsC1A1 = len(C1Inter & A1Inter)
                if(len(A1Inter) < 1):
                    continue
                supPP = newsNumsC1A1 / newsNums  # 计算单个属性集合对应的支持度
                confiPP = newsNumsC1A1/len(A1Inter)  # 计算置信度

                # 写下满足阈值的分类规则
                if(supPP >= minsupPP and confiPP >= minconfiPP):
                    fwrite.write("PP" + "|" + "supPP:" + str(supPP) + ","
                                 + "confiPP:" + str(confiPP) + ",")
                    for valA in A1:
                        fwrite.write(valA + " ")
                    fwrite.write("--")
                    for valC in C1:
                        fwrite.write(valC + " ")
                    fwrite.write("\n")
                    fwrite.flush()

            # 判断共同不具有负属性的文档相关参数值,每个三支概念形式为(X,(A1C1,A2C2))
            A1 = set([i for i in posAttr if i not in labelindex])
            C2 = set([i for i in negAttr if i in labelindex])
            if(A1.union(C2) not in A1C2Combine):
                A1C2Combine.append(A1.union(C2))
                C2Inter = set(newsNumsList)
                if (C2 == set([])):
                    continue
                for val in tuple(C2):
                    C2Inter = C2Inter & attrnotobjectdic[val]
                newsNumsA1C2 = len(A1Inter & C2Inter)
                supPN = newsNumsA1C2/newsNums
                confiPN = newsNumsA1C2 / len(A1Inter)

                if (supPN >= minsupPN and confiPN >= minconfiPN):
                    fwrite.write("PN" + "|" + "supPN:" + str(supPN) + ","
                                 + "confiPN:" + str(confiPN)+ ",")
                    for valA in A1:
                        fwrite.write(valA + " ")
                    fwrite.write("--")
                    for valC in C2:
                        fwrite.write(valC + " ")
                    fwrite.write("\n")
                    fwrite.flush()


if __name__ == "__main__":
    rootpath = "F:/englisgpaper2/UCI/"
    trainPath = rootpath + "trainData.txt"
    contextTrPath = rootpath + "ContextTr.txt"

    objNums = len(open(trainPath, 'r').readlines())   #训练集对象数
    print "objNums: ", objNums
    attrNums = len(open(contextTrPath, 'r').readlines())
    print "attrNums: ", attrNums

    labelindex = ['27', '28', '29', '30']

    outPath = rootpath + "out.txt"
    rulesPath = rootpath + "rules.txt"
    attrobjectdic = attrobjectDic(contextTrPath)
    attrnotobjectdic = attrnotobjectDic(objNums, contextTrPath)
    threeRules_fcbo(attrNums, outPath, rulesPath, objNums,
                  attrobjectdic, attrnotobjectdic, labelindex)
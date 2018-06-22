# -*- coding:utf-8-*-

from __future__ import division
from classifiByThreeConcepts import JieBaContext_1
minsupPP = 0.01
minsupPN = 0.01

# 构建字典，表示属性被那些对象拥有
def attrobjectDic(contextTrpath):
    ffile = open(contextTrpath, 'r')
    attrobjectdic = {}
    nums = 0
    newsList = []                         #为了计算出新闻文本的个数
    for line in ffile.readlines():
        lineList = line.strip(" \r\n").split(" ")
        attrobjectdic[str(nums)] = set(lineList)
        newsList.extend(lineList)
        nums += 1
    return attrobjectdic, len(set(newsList))

#构建字典，表示属性不被那些对象拥有
def attrnotobjectDic(newsNums, contextTrpath):
    ffile = open(contextTrpath, 'r')
    attrnotobjectdic = {}
    indexList = []
    for i in range(newsNums):
        indexList.append(str(i))
    nums = 0
    for line in ffile.readlines():
        listtmp = []
        lineList = line.strip(" \r\n").split(" ")
        for v in indexList:
            if(v not in lineList):
                listtmp.append(v)
        attrnotobjectdic[str(nums)] = set(listtmp)
        nums += 1
    return attrnotobjectdic

#构建字典，表示对象拥有那些属性
def objectattrDic(reducedPath):
    f = open(reducedPath, 'r')
    news = 0
    objectattrdic = {}
    for line in f.readlines():
        objectattrdic[str(news)] = set(line.strip(" \r\n").split(" "))
        news += 1
    return objectattrdic

#构建字典，表示对象不拥有那些属性
def notobjectattrDic(allwordsindex, reducedPath):
    f = open(reducedPath, 'r')
    news = 0
    notobjectattrdic = {}
    for line in f.readlines():
        lineList = line.strip(" \r\n").split(" ")
        notobjectattrdic[str(news)] = set([i for i in allwordsindex if i not in lineList])
        news += 1
    return notobjectattrdic

# 根据fcbo算法计算三支概念（已经正负属性）
def threeRules_fcbo(outPath, tconceptsPath, newsNums,
           attrobjectdic, attrnotobjectdic, labelindex):
    fwrite = open(tconceptsPath, 'w+')
    nums = 0
    A1C1Combine = []
    A1C2Combine = []
    with open(outPath, 'r') as f:
        for elem in f:
            if(elem.strip("\r\n") != "|"):
                nums += 1
                attrList = elem.strip(" \r\n").split("|")[1].split(" ")
                positiveattr = set([i for i in attrList if int(i) <= 489])
                negativeattr = set([str(int(j)-490) for j in attrList if int(j) > 489])
                newsNumsList = [str(k) for k in range(newsNums)]

                # 判断共同具有正属性的文档相关参数值,每个三支概念形式为(X,(A1C1,A2C2))
                if(positiveattr not in A1C1Combine):
                    A1C1Combine.append(positiveattr)
                    C1 = set([i for i in positiveattr if i in labelindex])
                    A1 = set([i for i in positiveattr if i not in labelindex])
                    C1Inter = set(newsNumsList)
                    A1Inter = set(newsNumsList)
                    if (C1 == set([])):
                        C1Inter = set()
                    if (C1 != set([])):
                        for val in tuple(C1):
                            C1Inter = C1Inter & attrobjectdic[val]
                    if (A1 == set([])):
                        A1Inter = set()
                    if (A1 != set([])):
                        for val in tuple(A1):
                            A1Inter = A1Inter & attrobjectdic[val]
                    newsNumsC1A1 = len(C1Inter & A1Inter)
                    supPP = newsNumsC1A1/newsNums    # 计算单个属性集合对应的支持度

                    # 写下满足阈值的分类规则
                    if(A1 != set([]) and C1 != set([]) and supPP >= minsupPP):
                        fwrite.write("PP" + "|" + "supPP:" + str(supPP) + ",")
                        for valA in A1:
                            fwrite.write(valA + " ")
                        fwrite.write("--")
                        for valC in C1:
                            fwrite.write(valC + " ")
                        fwrite.write("\n")
                        fwrite.flush()

                # 判断共同不具有负属性的文档相关参数值,每个三支概念形式为(X,(A1C1,A2C2))
                A1 = set([i for i in positiveattr if i not in labelindex])
                C2 = set([i for i in negativeattr if i in labelindex])
                if(A1.union(C2) not in A1C2Combine):
                    A1C2Combine.append(A1.union(C2))
                    C2Inter = set(newsNumsList)
                    if (C2 == set([])):
                        C2Inter = set()
                    if (C2 != set([])):
                        for val in tuple(C2):
                            C2Inter = C2Inter & attrnotobjectdic[val]
                    newsNumsA1C2 = len(A1Inter & C2Inter)
                    supPN = newsNumsA1C2/newsNums
                    if (A1 != set([]) and C2 != set([]) and supPN >= minsupPN):
                        fwrite.write("PN" + "|" + "supPN:" + str(supPN) + ",")
                        for valA in A1:
                            fwrite.write(valA + " ")
                        fwrite.write("--")
                        for valC in C2:
                            fwrite.write(valC + " ")
                        fwrite.write("\n")
                        fwrite.flush()


#根据cbo3c算法计算三支概念
def threeRules(outPath, tconceptsPath, newsNums,
                 objectattrdic, notobjectattrdic,
                 allwordsindex, labelindex):
    fobject = open(outPath, 'r')
    fwrite = open(tconceptsPath, 'w+')
    nums = 0
    for elem in fobject.readlines():
        if(elem.strip("\r\n") != "|"):
            nums += 1
            if(nums % 1000 == 0):
                print nums

            objectTup = tuple(elem.strip("\r\n").split("|")[1].split(" "))
            interSet = set(allwordsindex)
            notinterSet = set(allwordsindex)

            # 假设每个三支概念形式为(X, (A1C1,A2C2))
            for n in objectTup:
                interSet = interSet & objectattrdic[n]
            A1C1 = tuple(interSet)

            for m in objectTup:
                notinterSet = notinterSet & notobjectattrdic[m]
            A2C2 = tuple(notinterSet)

            newsNumsList = []
            for i in range(newsNums):
                newsNumsList.append(str(i))

            # 判断共同具有正属性的文档相关参数值
            C1 = set([i for i in A1C1 if i in labelindex])
            A1 = set([i for i in A1C1 if i not in labelindex])
            C1Inter = set(newsNumsList)
            A1Inter = set(newsNumsList)

            if (C1 == set([])):
                C1Inter = set()
            if (C1 != set([])):
                for val in tuple(C1):
                    C1Inter = C1Inter & attrobjectdic[val]
            if (A1 == set([])):
                A1Inter = set()
            if (A1 != set([])):
                for val in tuple(A1):
                    A1Inter = A1Inter & attrobjectdic[val]
            newsNumsC1A1 = len(C1Inter & A1Inter)

            # 判断共同不具有负属性的文档相关参数值
            C2 = set([i for i in A2C2 if i in labelindex])
            A2 = set([i for i in A2C2 if i not in labelindex])
            C2Inter = set(newsNumsList)
            A2Inter = set(newsNumsList)

            if (C2 == set([])):
                C2Inter = set()
            if (C2 != set([])):
                for val in tuple(C2):
                    C2Inter = C2Inter & attrnotobjectdic[val]
            if (A2 == set([])):
                A2Inter = set()
            if (A2 != set([])):
                for val in tuple(A2):
                    A2Inter = A2Inter & attrnotobjectdic[val]
            newsNumsA1C2 = len(A1Inter & C2Inter)
            newsNumsA2C1 = len(A2Inter & C1Inter)

            # 计算单个属性集合对应的支持度，用于后面求分类规则支持度和置信度,
            # 每个三支概念形式为(X, (A1C1,A2C2))
            supA1C1 = newsNumsC1A1/newsNums
            supA1C2 = newsNumsA1C2/newsNums
            supA2C1 = newsNumsA2C1/newsNums

            # 计算支持度
            supPP = supA1C1
            supPN = supA1C2

            # 写下满足阈值的分类规则
            if(A1 != set([]) and C1 != set([]) and supPP >= minsupPP):
                fwrite.write("PP" + "|" + "supPP:" + str(supPP) + ",")
                for valA in A1:
                    fwrite.write(valA + " ")
                fwrite.write("--")
                for valC in C1:
                    fwrite.write(valC + " ")
                fwrite.write("\n")
            if (A1 != set([]) and C2 != set([]) and supPN >= minsupPN):
                fwrite.write("PN" + "|" + "supPN:" + str(supPN) + ",")
                for valA in A1:
                    fwrite.write(valA + " ")
                fwrite.write("--")
                for valC in C2:
                    fwrite.write(valC + " ")
                fwrite.write("\n")

if __name__ == "__main__":
    rootpath = "F:/graduationThesis/dataSet/test/classifiByThreeConcepts/"
    newsSelectNums = 75
    JiebaPath = rootpath + "traindata_" + str(newsSelectNums) + "_Jieba.txt"
    wordsList, labelList = JieBaContext_1.labelwordsList(JiebaPath)
    allwords = wordsList + labelList

    labelindex = []
    for key in labelList:                          # label在allwords中对应的索引
        labelindex.append(str(allwords.index(key)))
    print labelindex
    wordsindex = []
    for key in wordsList:
        wordsindex.append(str(allwords.index(key)))
    allwordsindex = wordsindex + labelindex

    contextTrpath = rootpath + "contextTr.txt"
    reducedPath = rootpath + "contextreduced.txt"

    attrobjectdic, newsNums = attrobjectDic(contextTrpath)
    attrnotobjectdic = attrnotobjectDic(newsNums, contextTrpath)
    # objectattrdic = objectattrDic(reducedPath)
    # notobjectattrdic = notobjectattrDic(allwordsindex, reducedPath)
    # outPath = "F:/zhuxiaomin/out_file.txt"
    # tconceptsPath = "F:/graduationThesis/dataSet/test/classifiByThreeConcepts/" \
    #                 "rules_threeconcepts.txt"
    outPath = "F:/zhuxiaomin/out11.txt"
    tconceptsPath = rootpath + "rules_threeconcepts3.txt"
    threeRules_fcbo(outPath, tconceptsPath, newsNums,
                  attrobjectdic, attrnotobjectdic, labelindex)
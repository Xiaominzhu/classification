# -*- coding:utf-8-*-
import jieba
jieba.load_userdict("F:/englisgpaper2/text/words/addDict.txt")
from jieba import analyse
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

usenature = ("Ag", "ad", "an", "b", "dg", "g", "h", "i",
          "j", "k", "l", "Ng", "n", "nr", "ns", "nt", "nz",
          "s", "tg", "t", "vg", "v", "vd", "vn", "x", "z", "un")

#数据预处理部分
def selecttext(rootpath, newsSelectNums):
    namelist = os.listdir(rootpath)
    for n in namelist:
        print "n: ", n
        textname = os.path.splitext(n)[0]
        if(textname.find("_") == -1):
            f = open(rootpath + "/" + n, 'r')
            pathwrite = rootpath + "/" + textname + "_" + str(newsSelectNums) + ".txt"
            fwrite = open(pathwrite, "w+")
            linenums = 0
            for line in f.readlines():
                linenums += 1
                if(linenums <= newsSelectNums):
                    fwrite.write(line)

#数据预处理部分
def combinetext(writePath, path, classNums, newsSelectNums):
    fwrite = open(writePath, "w+")
    namelist = os.listdir(path)
    classnums = 1
    for n in namelist:
        if(classnums <= classNums):
            textname = os.path.splitext(n)[0]
            if(textname.find("_" + str(newsSelectNums)) != -1):
                classnums += 1
                f = open(path + "/" + n, "r")
                for line in f.readlines():
                    fwrite.write(line)

#基于标题分词，并基于tfidf提取特征词
def jiebase(readPath, JiebaPath):
    fstop = "F:/englisgpaper2/text/words/stopWords.txt"
    stopwords = [line.strip("\r\n") for line in open(fstop, 'r').readlines()]
    fstop_sports = "F:/englisgpaper2/text/words/stopWords_sports.txt"
    stopwords_sports = [line.strip("\r\n") for line in
                            open(fstop_sports, 'r').readlines()]
    stopwordsSet_all = set(stopwords + stopwords_sports)
    f = open(readPath, 'r')
    fwrite = open(JiebaPath, 'w+')
    lineNums = 0
    analyse.set_stop_words("F:/englisgpaper2/text/words/stopWords.txt")     #加载停用词
    for line in f.readlines():
        lineNums += 1
        lineList = line.strip("\r\n").split(":::")
        lineClass = lineList[0]
        lineTitle = lineList[1].split(" title ")[0]
        seg_title = analyse.extract_tags(lineTitle, topK=7, allowPOS=usenature)
        # seg_title = list(jieba.cut(lineTitle, cut_all=False))
        fwrite.write(lineClass.encode('utf-8') + ":::")
        for w in seg_title:
            tmpval = w.encode('utf-8')
            # for key, values in synonymdic.items():
            #     if(tmpval in values):
            #         tmpval = key
            if(tmpval not in stopwordsSet_all):
                fwrite.write(tmpval + ",")
        fwrite.write("\n")

# 标题分词和内容分词，并基于tfidf提取特征词
def jiebase_content(readPath, JiebaPath, contentNums):
    fstop = "F:/graduationThesis/dataSet/test/stopWords.txt"
    stopwords = [line.strip("\r\n") for line in open(fstop, 'r').readlines()]
    fstop_sports = "F:/graduationThesis/dataSet/test/stopWords_sports.txt"
    stopwords_sports = [line.strip("\r\n") for line in
                            open(fstop_sports, 'r').readlines()]
    stopwordsSet_all = set(stopwords + stopwords_sports)
    f = open(readPath, 'r')
    fwrite = open(JiebaPath, 'w+')
    lineNums = 0
    analyse.set_stop_words("F:/graduationThesis/dataSet/test/stopWords.txt")     #加载停用词
    for line in f.readlines():
        lineNums += 1
        lineList = line.strip("\r\n").split(":::")
        lineClass = lineList[0]
        lineTitle = lineList[1].split(" title ")[0]
        lineContent = lineList[1].split(" title ")[1]
        seg_title = analyse.extract_tags(lineTitle, topK=10, allowPOS=usenature)
        seg_content = analyse.extract_tags(lineContent, topK=contentNums, allowPOS=usenature)
        fwrite.write(lineClass.encode('utf-8') + ":::")
        for w in seg_title:
            tmpval = w.encode('utf-8')
            if (tmpval not in stopwordsSet_all):
                fwrite.write(tmpval + ",")
        for w_con in seg_content:
            tmpval_con = w_con.encode('utf-8')
            if (tmpval_con not in stopwordsSet_all):
                fwrite.write(tmpval_con + ",")
        fwrite.write("\n")

#训练集中标签列表、关键词列表
def labelwordsList(JiebaPath):
    f1 = open(JiebaPath, 'r')
    labelList = []
    wordsList = []
    for line in f1.readlines():
        lineList = line.strip(",\r\n").split(":::")
        labelList.append(lineList[0].replace('\xef\xbb\xbf', ''))
    f2 = open(JiebaPath, 'r')
    for line in f2.readlines():
        lineList = line.strip(",\r\n").split(":::")
        contentList = lineList[1].split(",")
        for wd in set(contentList):
            if (wd not in set(labelList)):
                wordsList.append(wd)
    #过滤被低于2篇文章拥有的特征词，以减少特征词维度
    wordCount = {}
    for words in wordsList:
        wordCount[words] = wordsList.count(words)
    wordsmoreone = []
    for key, val in wordCount.items():
        if(val >= 2):
            wordsmoreone.append(key)
    return wordsmoreone, list(set(labelList))

# 索引表示的形式背景（对象:新闻, 属性:特征词）
def context(allwords, JiebaPath, contextPath):
    f = open(JiebaPath, 'r')
    fwrite = open(contextPath, 'w+')
    newsNums = 0
    for line in f.readlines():
        newsNums += 1
        lineList = list(set(line.strip(",\r\n").split(":::")[1].split(",")))
        lineList.append(line.strip(",\r\n").split(":::")[0].replace('\xef\xbb\xbf', ''))
        usewords = []
        for i in range(len(lineList)):
            if(lineList[i] in allwords):
                usewords.append(str(allwords.index(lineList[i])))
        usewordsSetList = list(set(usewords))
        if(len(usewordsSetList) >= 4):         #该文本至少含有一个关键词，另一个为类别属性
            for v in range(len(usewordsSetList) - 1):
                fwrite.write(usewordsSetList[v] + " ")
            fwrite.write(usewordsSetList[-1] + "\n")
    return newsNums

# 删除具有相同行的形式背景
def reducecontext(contextPath, reducePath):
    f = open(contextPath, 'r')
    fwrite = open(reducePath, "w+")
    elemList = []
    for line in f.readlines():
        linestr = line.strip("\r\n")
        if(linestr not in elemList):
            elemList.append(linestr)
            fwrite.write(linestr + "\n")
    print "news numbers: ", len(elemList)

# 索引形式背景的转置（对象:特征词，属性:新闻）
def contextTr(allwords, reducePath, contextTrPath):
    f = open(reducePath, 'r')
    fwrite = open(contextTrPath, 'w+')
    newsWordsDic = {}
    newsNums = 0
    for line in f.readlines():
        newsWordsDic[str(newsNums)] = line.strip("\r\n").split(" ")
        newsNums += 1
    for i in range(len(allwords)):
        # fwrite.write(allwords[i].encode("utf-8") + "," + str(i) + ":")
        for items in newsWordsDic.items():
            if(str(i) in items[1]):
                fwrite.write(items[0] + " ")
        fwrite.write("\n")

# 形式背景与补形式背景的并置，对象：文本，属性：关键词
def binaryContext(reducePath, combineContext, allwords):
    f = open(reducePath, 'r')
    fwrite = open(combineContext, 'w+')
    wordslen = len(allwords)
    allWordsindex = [i+wordslen for i in range(wordslen)]
    for line in f.readlines():
        lineList = line.strip(" \r\n").split(" ")
        for j in lineList:
            fwrite.write(j + " ")
        for r in allWordsindex:
            if (str(r - wordslen) not in lineList):
                fwrite.write(str(r) + " ")
        fwrite.write("\n")

if __name__ == "__main__":
    rootpath = "F:/englisgpaper2/text/"
    path = "F:/englisgpaper2/text/train_tmp/"
    # newsSelectNums = 30
    # selecttext(path, newsSelectNums)
    # writePath = rootpath + "traindata_" + str(newsSelectNums) + ".txt"
    # classNums = 4
    # combinetext(writePath, path, classNums, newsSelectNums)
    readPath = rootpath + "traindata_20.txt"
    JiebaPath = rootpath + "train_jieba.txt"
    jiebase(readPath, JiebaPath)

    wordsList, labelList = labelwordsList(JiebaPath)
    allwords = wordsList + labelList
    labelindex = []
    for key in labelList:                          # label在allwords中对应的索引
        labelindex.append(str(allwords.index(key)))
    wordsindex = []
    for key in wordsList:
        wordsindex.append(str(allwords.index(key)))

    contextPath = rootpath + "context.txt"
    newsNums = context(allwords, JiebaPath, contextPath)
    reducePath = rootpath + "contextreduced.txt"
    reducecontext(contextPath, reducePath)
    contextTrPath = rootpath + "contextTr.txt"
    newsNums = contextTr(allwords, reducePath, contextTrPath)
    combineContext = rootpath + "combineContext.txt"
    binaryContext(reducePath, combineContext, allwords)





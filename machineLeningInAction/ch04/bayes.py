from numpy import *
import re
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        # 取并集
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):
    # 创建一个其中所含元素都为0的向量
    returnVec = [0] * len(vocabList)
    # 遍历每个词条
    for word in inputSet:
        if word in vocabList:
            # 如果词条存在于词汇表中，则置1
            # index返回word出现在vocabList中的索引
            # 若这里改为+=则就是基于词袋的模型，遇到一个单词会增加单词向量中德对应值
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary" % word)
    # 返回文档向量
    return returnVec


"""
训练算法，从词向量计算概率p(w0|ci)...及p(ci)
    :param trainMatrix: 由每篇文档的词条向量组成的文档矩阵
    :param trainCategory: 每篇文档的类标签组成的向量
    :return: 
    """
def trainNB0(trainMatrix,trainCategory):
    # 获取文档居中中文档的数目
    numTrainDocs = len(trainMatrix)
    # 获取词条向量的长度
    numWords = len(trainMatrix[0])
    # 所有文档中属于类1所占的比例
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    # 创建一个长度为词条向量等长的列表
    p0Num = ones(numWords);p1Num = ones(numWords)
    p0Denom = 2.0;p1Denom = 2.0
    # 遍历每一篇文档的词条向量
    for i in range(numTrainDocs):
    #   如果该词条向量的对应标签为1
        if trainCategory[i] == 1:
    #         统计所有类别为1的词条向量中各个词条出现的次数
            p1Num += trainMatrix[i]
    #         统计类别为1的词条向量中出现所有词条的总数
    #         即统计类1所有文档中出现单词的数目
            p1Denom+=sum(trainMatrix[i])
        else:
    #     统计所有类别为0的词条向量中各个词条出现的次数
            p0Num += trainMatrix[i]
            #         统计类别为0的词条向量中出现所有词条的总数
            #         即统计类0所有文档中出现单词的数目
            p0Denom += sum(trainMatrix[i])
#
#     利用Numpy数组计算p(wi|c1)
    p1vect = log(p1Num/p1Denom)#     为避免下溢问题，后面会改成log()

    p0Vect = log(p0Num/p0Denom)#     为避免下溢问题，后面会改成log()
    return p0Vect,p1vect,pAbusive


"""
朴素贝叶斯分类函数
  :param vec2Classify: 朴素贝叶斯分类函数
  :param p0Vec: 类别0所有文档中各个词条出现的频数p(wi|c0)
  :param p1Vec: 类别1所有文档中各个词条出现的频数p(wi|c1)
  :param pClass1: 类别为1的文档占文档总数比例
  :
  """
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
# 根据朴素贝叶斯分类函数分别计算待分类文档属于类1和类0的概率
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0


"""
分类测试整体函数 
    :return: 
    """
def testingNB():
    # 由数据集获取文档矩阵和类标签向量
    listOPosts, listClasses = loadDataSet()
   #统计所有文档中出现的词条，存入词条列表
    myVocabList=createVocabList(listOPosts)
 #创建新的列表
    trainMat=[]
    for postinDoc in listOPosts:
        #将每篇文档利用words2Vec函数转为词条向量，存入文档矩阵中
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))\
    #将文档矩阵和类标签向量转为NumPy的数组形式，方便接下来的概率计算
    #调用训练函数，得到相应概率值
    p0V,p1V,pAb=trainNB0(array(trainMat),array(listClasses))
#测试文档
    testEntry=['love','my','dalmation']
    #将测试文档转为词条向量，并转为NumPy数组的形式
    thisDoc=array(setOfWords2Vec(myVocabList,testEntry))
 #利用贝叶斯分类函数对测试文档进行分类并打印
    print(testEntry,'classified as:',classifyNB(thisDoc,p0V,p1V,pAb))

#第二个测试文档
    testEntry1=['stupid','garbage']
    #同样转为词条向量，并转为NumPy数组的形式
    thisDoc1=array(setOfWords2Vec(myVocabList,testEntry1))
    print(testEntry1,'classified as:',classifyNB(thisDoc1,p0V,p1V,pAb))


def bagOfWord2VecMN(vocabList,inputSet):
#     词袋向量
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
#             某词没出现一次，次数加1
            returnVec[vocabList.index(word)] += 1
    return returnVec

def testParse(bigString):
    listOfTokens = re.split(r'\W*',bigString)
    return [tok.lower for tok in listOfTokens if len(tok)>2]


def spamTest():
    docList = []
    classList = []
    fullText = []
    # 遍历25个txt文件
    for i in range(1, 26):
        # 读取每个垃圾邮件，并以字符串转换成字符串列表
        wordList = testParse(open('email/spam/%d.txt' % i, 'r').read())
        docList.append(wordList)
        fullText.append(wordList)
        # 标记垃圾邮件，1表示垃圾文件
        classList.append(1)
        # 读取每个非垃圾邮件，并以字符串转换成字符串列表
        wordList = testParse(open('email/ham/%d.txt' % i, 'r',encoding='ISO-8859-1').read())
        docList.append(wordList)
        fullText.append(wordList)
        # 标记非垃圾邮件，0表示非垃圾文件
        classList.append(0)
    # 创建词汇表，不重复
    vocabList = createVocabList(docList)
    # 创建存储训练集的索引值的列表和测试集的索引值的列表
    trainingSet = list(range(50))
    testSet = []
    # 从50个邮件中，随机挑选出40个作为训练集，10个作为测试集
    for i in range(10):
        # 随机选取索引值,随机生成一个实数
        randIndex = int(random.uniform(0, len(trainingSet)))
        # 添加测试集的索引值
        testSet.append(trainingSet[randIndex])
        # 在训练集列表中删除添加到测试集的索引值
        del(trainingSet[randIndex])
    # 创建训练集矩阵和训练集类别标签向量
    trainMat = []
    trainClasses = []
    # 遍历训练集
    for docIndex in trainingSet:
        # 将生成的词集模型添加到训练集矩阵中
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        # 将类别添加到训练集类别标签向量中
        trainClasses.append(classList[docIndex])
    # 训练朴素贝叶斯模型
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))
    # 错误分类计数
    errorCount = 0
    # 遍历测试集
    for docIndex in testSet:
        # 测试集的词集模型
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        # 如果分类错误
        if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            # 错误计数器加1
            errorCount += 1
            print("分类错误的测试集：", docList[docIndex])
    print("错误率：%.2f%%" % (float(errorCount) / len(testSet) * 100))
# def spamTest():
#     #新建三个列表
#     docList=[];classList=[];fullTest=[]
#     #i 由1到26
#     for i in range(1,26):
#         #打开并读取指定目录下的本文中的长字符串，并进行处理返回
#         wordList=testParse(open('email/spam/%d.txt' %i).read())
#         #将得到的字符串列表添加到docList
#         docList.append(wordList)
#         #将字符串列表中的元素添加到fullTest
#         fullTest.extend(wordList)
#         #类列表添加标签1
#         classList.append(1)
#         #打开并取得另外一个类别为0的文件，然后进行处理
#
#         print(i)
#         wordList = testParse(open('email/ham/%d.txt' % i,encoding='ISO-8859-1').read())
#
#         docList.append(wordList)
#         fullTest.extend(wordList)
#         classList.append(0)
#     #将所有邮件中出现的字符串构建成字符串列表
#     vocabList=createVocabList(docList)
#     #构建一个大小为50的整数列表和一个空列表
#     # python3.x
#     # range返回的是range对象，不返回数组对象
#     trainingSet=list(range(50));testSet=[]
#     #随机选取1~50中的10个数，作为索引，构建测试集
#     for i in range(10):
#         #随机选取1~50中的一个整型数
#         randIndex=int(random.uniform(0,len(trainingSet)))
#         #将选出的数的列表索引值添加到testSet列表中
#         testSet.append(trainingSet[randIndex])
#         #从整数列表中删除选出的数，防止下次再次选出
#         #同时将剩下的作为训练集
#
#         del (trainingSet[randIndex])
#     #新建两个列表
#     trainMat=[];trainClasses=[]
#     #遍历训练集中的吗每个字符串列表
#     for docIndex in trainingSet:
#         #将字符串列表转为词条向量，然后添加到训练矩阵中
#         trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
#         #将该邮件的类标签存入训练类标签列表中
#         trainClasses.append(classList[docIndex])
#     #计算贝叶斯函数需要的概率值并返回
#     p0V,p1V,pSpam=trainNB0(array(trainMat),array(trainClasses))
#     errorCount=0
#     #遍历测试集中的字符串列表
#     for docIndex in testSet:
#         #同样将测试集中的字符串列表转为词条向量
#         wordVector=setOfWords2Vec(vocabList,docList[docIndex])
#         #对测试集中字符串向量进行预测分类，分类结果不等于实际结果
#         if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
#             errorCount+=1
#     print('the error rate is:',float(errorCount)/len(testSet))














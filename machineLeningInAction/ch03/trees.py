from math import log
import operator
import pickle
import numpy as np
#计算给定数据集的香农熵（信息熵）
def calcShannonEnt(dataSet):
    numEntrues = len(dataSet)
    labelCounts = {}
    for featvec in dataSet:
        currentLabel = featvec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1

    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntrues
        shannonEnt -= prob*log(prob,2)
        print("key:%d---prob:%d--labelCounts[key]:%d---numEntrues:%d",(key,prob,labelCounts[key],numEntrues))
    return shannonEnt

# 创造模拟数据
def createDataSet():
    dataSet = [[1,1,'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    return dataSet,labels

# 划分数据集
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedDeatVec = featVec[:axis]
            reducedDeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedDeatVec)
    return retDataSet

# 选择最好的数据集的划分方式
def chooseBestFeatureToSplit(dataSet):
    numFeatrues = len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatrues):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
            infoGain = baseEntropy - newEntropy
            if(infoGain > bestInfoGain):
                bestInfoGain = infoGain
                bestFeature = i
        return bestFeature

    # 网上的参考解释
    # def chooseBestFeatureToSplit(dataset):
    #     numFeature = len(dataset[0]) - 1
    #     # 特征个数的获取是第一行的长度-1，具体还是要看数据集的
    #     baseEntropy = calcShannonEnt(dataset)
    #     # 计算划分前的信息熵
    #     bestInfoGain = 0.0
    #     bestFeature = -1
    #     # 初始化最优信息增益和最优特征
    #
    #     for i in range(numFeature):
    #         featList = [example[i] for example in dataset]
    #         # 相当于取dataset第i列的值
    #         unique = set(featList)
    #         # 由set类型转为来求取不重复的值
    #         newEntropy = 0.0
    #         # 设置第i维划分后信息熵为00
    #         for value in unique:
    #             subDataset = splitDataset(dataset, i, value)
    #             # 针对第i维的每一种取值划分子数据集
    #             prob = float(len(subDataset)) / len(dataset)
    #             newEntropy += prob * calcShannonEnt(subDataset)
    #             # 第i维特征每一种取值的信息熵叠加
    #         infoGain = baseEntropy - newEntropy
    #         # 第i维的信息增益
    #         if (infoGain > bestInfoGain):
    #             bestFeature = i
    #             bestInfoGain = infoGain
    #             # 如果该维信息增益大于当前最大信息增益，则替换
    #     return bestFeature
    #
    # ---------------------
    # 作者：从兮
    # 来源：CSDN
    # 原文：https: // blog.csdn.net / dai_fun / article / details / 50989043
    # 版权声明：本文为博主原创文章，转载请附上博文链接！


#
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(),
                              key = operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

# 创建树的函数代码
def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]#stop splitting when all of the classes are equal
    if len(dataSet[0]) == 1: #stop splitting when there are no more features in dataSet
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    subLabels = labels[:]
    del (subLabels[bestFeat])
    # del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = subLabels[:]       #copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)
    return myTree

 #    书本存在漏洞
 # del(labels[bestFeat])    # del 会直接修改原数据  造成 ‘no surfacing‘ is not in list 的错误
    subLabels = labels[:]
    del (subLabels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

#网络参考
# def createTree(dataSet, labels):
#     # 此处有必要注释一下，labels表示的不是数据分类类别的标签，而是特征的标签
#     classlist = [example[-1] for example in dataSet]
#     # 从dataSet最后一列中获取类标签列表
#     if classlist.count(classlist[0]) == len(classlist):
#         return classlist[0]
#     # 此处为递归终止的第一种情况：子集内所有类标签一样
#     # classlist以第一项元素的标签计数，如果等于列表个数，说明列表中值都是一样的
#
#     if len(dataSet[0]) == 1:
#         return majorityCnt(classlist)
#     # 递归终止的另一情况：已经划分完所有属性特征
#     # len(dataSet[0])==1表示划分到最后只剩下一列类别标签
#
#     bestFeat = chooseBestFeatureToSplit(dataSet)
#     # 针对当前数据集选择最优划分特征
#
#     bestFeatLabel = labels[bestFeat]
#     # 获得对应的维度标签
#     myTree = {bestFeatLabel: {}}
#     # 建立当前树结点，即维度标签及空值
#     del (labels[bestFeat])
#     # 将已选维度标签从标签列表中删除
#     featValues = [example[bestFeat] for example in dataSet]
#     # 获取该维度的值
#     uniqueValues = set(featValues)
#     # 获得不重复的值
#     for value in uniqueValues:
#         # 对最优维度的每个值进行操作，一个值对应一个分支
#         sublabels = labels[:]
#         # 复制获得子维度标签，此时labels中已删除当前最优维度标签
#         myTree[bestFeatLabel][value] = createTree(splitDataset(dataSet, bestFeat, value), sublabels)
#         # 递归对每个分支建立子树。使用到了之前的splitdataset划分子树函数
#     return myTree

def classify(input_tree, feat_labels, test_vec):
    """使用决策树分类测试数据"""
    first_str = list(input_tree.keys())[0]
    second_dict = input_tree[first_str]
    # 使用index方法查找当前列表中第一个匹配firstStr变量的元素
    feat_index = feat_labels.index(first_str)
    # 遍历整棵树
    for key in second_dict.keys():
        # 如果测试数据的属性值等于Key的值
        if test_vec[feat_index] == key:
            # 判断是否为字典类型，如果是字典类型，则说明不是叶子节点，得需要递归
            # 这里判断得出类别，就是寻找是否是字典类型，如果是字典类型，则不是叶子节点，如果不是字典类型，则说明是叶子结点
            if type(second_dict[key]).__name__ == 'dict':
                class_label = classify(second_dict[key], feat_labels, test_vec)
            else:
                class_label = second_dict[key]
    return class_label

# 与书本比较  w+改为wb+,r+改为rb+
# 使用pickle模块存储决策树
def storeTree(inputTree,filename):
    np.save(filename,inputTree)
    # fw = open(filename,'wb+')
    # pickle.dump(inputTree,fw)
    # fw.close()


def grabTree(filename):
    reload_myTree = np.load(filename).item()
    return reload_myTree
    # fr = open(filename,'rb')
    # return pickle.load(fr)





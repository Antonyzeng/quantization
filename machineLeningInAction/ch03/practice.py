import trees
import matplotlib
import matplotlib.pyplot as plt
from numpy import *
import treePlotter
myDat,labels = trees.createDataSet()
print(myDat)

# print(trees.calcShannonEnt(myDat))
# data_set = trees.splitDataSet(myDat, 0, 1)
# print(data_set)


print(trees.chooseBestFeatureToSplit(myDat))

myTree = trees.createTree(myDat, labels)
print(myTree)

# treePlotter.createPlot()


# 由于回退代码,部分代码丢失
trees.storeTree(myTree,'classifierStorage.npy')
tree= trees.grabTree('classifierStorage.npy')
print(tree)


# print(tree)



fr = open('lenses.txt')
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
# :age(年龄)、prescript(症状)、astigmatic(是否散光)、tearRate(眼泪数量)
lensesLabels=['age','prescript','astigmatic','tearRate']
lensesTree = trees.createTree(lenses,lensesLabels)
print(lensesTree)

treePlotter.createPlot(lensesTree)

print(trees.classify(myTree,labels,[1,0]))
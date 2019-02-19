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

treePlotter.createPlot()









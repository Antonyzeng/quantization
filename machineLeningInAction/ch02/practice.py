import KNN
import matplotlib
import matplotlib.pyplot as plt
from numpy import *
group,labels = KNN.createDataSet()
classify_ = KNN.classify0([1, 1], group, labels, 3)
#print(classify_)

datingDataMat,datingLabels = KNN.file2matrix('datingTestSet2.txt')

#print(datingDataMat)
#print(datingLabels)


normMat,ranges,minVals = KNN.autoNorm(datingDataMat)
#print(normMat)


# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(normMat[:,0],normMat[:,1],s=100.0*array(normMat),c=1.0*array(normMat))
#
# plt.show()


# KNN.datingClassTest()

# KNN.classifyPerson()


KNN.handwritingClassTest()












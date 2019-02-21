import matplotlib.pyplot as plt

# 使用文本注解绘制树节点

decisionNode = dict(boxstyle = 'sawtooth',fc = '0.8')
leafNode = dict(boxstyle='round4',fc='0.8')
arrow_args = dict(arrowstyle = '<-')


def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords = 'axes fraction',xytext=centerPt,textcoords='axes fraction',
                            va='center',ha='center',bbox=nodeType,arrowprops=arrow_args)


def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)

def plotTree(myTree, parentPt, nodeTxt):#if the first key tells you what feat was split on
    numLeafs = getNumLeafs(myTree)  #this determines the x width of this tree
    depth = getTreeDepth(myTree)
    # 书本需要修改
    firstList = list(myTree.keys())
    firstStr = firstList[0]     #the text label for this node should be this
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            plotTree(secondDict[key],cntrPt,str(key))        #recursion
        else:   #it's a leaf node print the leaf node
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD
#if you do get a dictonary you know it's a tree, and the first element will be another dict



def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)    #no ticks
    #createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree, (0.5,1.0), '')
    plt.show()

#def createPlot():
#    fig = plt.figure(1, facecolor='white')
#    fig.clf()
#    createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
#    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
#    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
#    plt.show()

# 获取叶结点的数目和树的层数

def getNumLeafs(myTree):
    numLeafs = 0
    # 书本需要修改
    firstList = list(myTree.keys())
    firstStr = firstList[0]
    
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    # 书本需要修改
    firstList = list(myTree.keys())
    firstStr = firstList[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1+getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth>maxDepth:
            maxDepth = thisDepth
    return maxDepth


# 该函数需要一个绘图区域
def plot_node(node_txt, center_pt, parent_pt, node_type):
    create_plot.ax1.annotate(node_txt, xy=parent_pt, xycoords='axes fraction',
                             xytext=center_pt, textcoords='axes fraction', va='center',
                             ha='center', bbox=node_type, arrowprops=arrow_args)


# cntr_pt指子节点的坐标，parent_pt指父节点的坐标，txt_string填充的文本消息
def plot_mid_text(cntr_pt, parent_pt, txt_string):
    """在父子节点间填充文本信息"""
    # 填充的位置在父节点和子节点中间位置
    xmid = (parent_pt[0] - cntr_pt[0]) / 2.0 + cntr_pt[0]
    ymid = (parent_pt[1] - cntr_pt[1]) / 2.0 + cntr_pt[1]
    create_plot.ax1.text(xmid, ymid, txt_string, va="center", ha="center", rotation=30)


# my_tree指树的信息，patent_pt指父节点的坐标，node_txt指标注的属性信息
def plot_tree(my_tree, parent_pt, node_txt):
    # 获取树的宽度
    num_leafs = getNumLeafs(my_tree)
    # 获取树的深度
    depth = getTreeDepth(my_tree)
    # 第一次划分数据集的类别标签
    first_str = list(my_tree.keys())[0]
    cntr_pt = (plot_tree.x_off + (1.0 + float(num_leafs)) / 2.0 / plot_tree.totalw, plot_tree.y_off)
    # print(cntr_pt, parent_pt)
    # 标记子节点属性值
    plot_mid_text(cntr_pt, parent_pt, node_txt)
    # 子节点标记标签
    plot_node(first_str, cntr_pt, parent_pt, decisionNode)
    # 第二个字典
    second_dict = my_tree[first_str]
    # 两个节点之间的距离间隔为：1.0/plot_tree.totald
    plot_tree.y_off = plot_tree.y_off - 1.0 / plot_tree.totald
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            plot_tree(second_dict[key], cntr_pt, str(key))
        else:
            plot_tree.x_off = plot_tree.x_off + 1.0 / plot_tree.totalw
            print(plot_tree.x_off)
            plot_node(second_dict[key], (plot_tree.x_off, plot_tree.y_off), cntr_pt, leaf_node)
            plot_mid_text((plot_tree.x_off, plot_tree.y_off), cntr_pt, str(key))
    plot_tree.y_off = plot_tree.y_off + 1.0 / plot_tree.totald


def create_plot(in_tree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    create_plot.ax1 = plt.subplot(111, frameon=False, **axprops)
    # plot_tree.totalw和plot_tree.totald存储书树的宽度和树的深度
    plot_tree.totalw = getNumLeafs(in_tree)
    plot_tree.totald = getTreeDepth(in_tree)
    # plot_tree.x_off和plot_tree.y_off追踪已经绘制的节点位置，以及放置下一个节点的恰当位置
    plot_tree.x_off = -0.5 / plot_tree.totalw
    # print(plot_tree.x_off)
    plot_tree.y_off = 1.0
    plot_tree(in_tree, (0.5, 1.0), '')
    plt.show()



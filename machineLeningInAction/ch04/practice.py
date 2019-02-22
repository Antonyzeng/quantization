import bayes
import re
from numpy import *
listOPosts,listClasses = bayes.loadDataSet()
myVocabList= bayes.createVocabList(listOPosts)
print(myVocabList)

print(bayes.setOfWords2Vec(myVocabList,listOPosts[0]))

trainMat = []
for postinDoc in listOPosts:
    trainMat.append(bayes.setOfWords2Vec(myVocabList,postinDoc))

print(trainMat[0])
p0v,p1v,pAb= bayes.trainNB0(trainMat,listClasses)
print(p1v)


bayes.testingNB()



# 垃圾邮件分类


# 切分文本
mySent = 'this book is the best book on Python or M.L. I have ever laid eyse upon'
regEx = re.compile('\\W*')
listOfTokens = regEx.split(mySent)
print(listOfTokens)
tok = mySent.split()
print(split)
['this', 'book', 'is', 'the', 'best', 'book', 'on', 'Python', 'or', 'M', 'L', 'I', 'have', 'ever', 'laid', 'eyse', 'upon']

['this', 'book', 'is', 'the', 'best', 'book', 'on', 'Python', 'or', 'M.L.', 'I', 'have', 'ever', 'laid', 'eyse', 'upon']

tok = [tok.lower() for tok in listOfTokens if len(tok) > 0]
print(tok)

emailText = open('email/ham/6.txt').read()
listOfTokens = regEx.split(emailText)



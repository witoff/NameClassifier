from nameLoader import NameLoader
from nltk import NaiveBayesClassifier as nbc, classify
import random

class NameClassifier(object):
  
  def __init__(self):
  
    #load all names
    nl = NameLoader()
    self.names = nl.getNames()

  def __getFeatures(self, name):
    name = name.lower()
    return {
      'last_letter' : name[-1], 
      'last_three'  : name[-3:],
      'first_two'   : name[:2],
      'z_count'     : name.count('z'),
      'double_a'    : bool(name.count('aa')),
      'length'      : len(name)}

  def buildFeatures(self):
    features = []
    for n in self.names:
      f = self.__getFeatures(n)
      label = 'M' if self.names[n]['M'] > self.names[n]['F'] else 'F'
      instance = (f, label)
      features.append(instance)

    #shuffle so we're not isolated on a single year
    random.shuffle(features)
    return features

  def train(self, foldPercent=.8):
    features = self.buildFeatures()

    foldIndex = int(foldPercent * len(features))
    self.setTrain = features[:foldIndex]
    self.setTest = features[foldIndex:]

    self.classifier = nbc.train(self.setTrain)

  def test(self):
    accuracy = classify.accuracy(self.classifier, self.setTest)
    print 'accuracy: ', accuracy
    return accuracy


  def classifyName(self, name):
    pc = self.classifier.prob_classify(self.__getFeatures(n))
    print 'Bayes Classification: ', pc.max(), pc.prob(pc.max())
    return pc.max()

  """ classify based on dictionay of names, or fallback on bayes if name doesn't exist"""
  def smartClassify(self, name):
    name = name.lower()
    if name in self.names:
      label = 'M' if self.names[name]['M'] > self.names[name]['F'] else 'F'
      counts = [self.names[name]['M'], self.names[name]['F']]
      confidence = float(max(counts))/sum(counts)
      print 'name existed. Classified as: ', label, ' confidence: ', confidence
    else:
      self.classifyName(name)

    

if __name__ == '__main__':
  nc = NameClassifier()
  nc.train()
  nc.test()

  names = ['rob', 'robert', 'roberta', 'sharon', 'Michael', 'Michelle', 'robtony', 'taifun']
  for n in names:
    print '\n', n
    nc.smartClassify(n)


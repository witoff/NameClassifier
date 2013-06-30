from nameClassifier import NameClassifier
import json
from collections import Counter



#tree = {'rob': {'matt':{}, 'tony':{}, 'liz':{}}, 'liz': {'bob':{}, 'chris':{}, 'jenn':{}, 'melissa':{}}}
f = open('data/nameTree.json', 'r')
tree = json.loads(f.read())
f.close()

nc = NameClassifier()
nc.train()
all_names = []
tuples = []
CLASSIFY_DEEP = False
def classifyTree(node, depth=0):
  count={'M':0, 'F':0}
  if node:
    for name in node:
      all_names.append(name)
      subCount = classifyTree(node[name], depth+1)
      if sum(subCount.values())>0:
        print '-'*depth, name, subCount
      label = nc.smartClassify(name)
      tuples.append((label, subCount))
      #print '-'*depth, name, label
      count[label] += 1
      if CLASSIFY_DEEP:
        for k in count:
          count[k] += subCount[k]
  return count


print classifyTree(tree)
print '\nTUPLES:'
f = open('tuples.csv', 'w')
totals = {'M': {'M': 0, 'F': 0}, 'F': {'M': 0, 'F': 0} }
for t in tuples:
  if sum(t[1].values())>0:
    line = "%s,%i,%i" % (t[0], t[1]['M'], t[1]['F'])
    f.write(line + '\n')
    print line
  for k in t[1]:
    totals[t[0]][k] += t[1][k]
f.close()

print 'totals: ', totals
print '\n\nTOTALS: '
print 'ratio of genders working for a gender'
pLikes = {}
for t in totals:
  print t 
  print '- ', totals[t]
  pLikes[t] = 100*float(totals[t][t])/sum(totals[t].values())
  print '- like: %.2f%%' % (pLikes[t])


print '\ntotal count: ', len(all_names)
exists = {'M':0, 'F':0}
for n in all_names:
  label = nc.smartClassify(n)
  exists[label] += 1
pExists = {}
for g in ['M', 'F']:
  print g
  print '- ', exists[g]
  pExists[g] = 100*float(exists[g])/sum(exists.values())
  print '- exist: %.2f%%' % (pExists[g])

bias = {}
print '\nBias:'
for g in pLikes:
  bias[g] = pLikes[g]-pExists[g]
  print '- ', g
  print '- bias: %.2f%%' % (bias[g])


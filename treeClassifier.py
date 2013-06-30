from nameClassifier import NameClassifier



tree = {'rob': {'matt':None, 'tony':None, 'liz':None}, 'liz': {'bob':None, 'chris':None, 'jenn':None, 'melissa':None}}

nc = NameClassifier()
nc.train()

tuples = []
def classifyTree(node, depth=0):
  count={'M':0, 'F':0}
  if node:
    for name in node:
      subCount = classifyTree(node[name], depth+1)
      print '-'*depth, name, subCount
      label = nc.smartClassify(name)
      tuples.append((label, subCount))
      #print '-'*depth, name, label
      count[label] += 1
      for k in count:
        count[k] += subCount[k]
  return count


print classifyTree(tree)
print '\nTUPLES:'

totals = {'M': {'M': 0, 'F': 0}, 'F': {'M': 0, 'F': 0} }
for t in tuples:
   print '-', t
   for k in t[1]:
     totals[t[0]][k] += t[1][k]

print '\nTOTALS: ' 
for t in totals:
  print t 
  print '- ', totals[t]
  print '- like: %.0f%%' % (100*float(totals[t][t])/sum(totals[t].values()))

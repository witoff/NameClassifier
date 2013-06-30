import json
from collections import Counter
from nameClassifier import NameClassifier

nc = NameClassifier()
nc.train()

## NAMES OVER TIME
f = open('data/orderedNames.json', 'r')
names = json.loads(f.read())
f.close()

def ratio(names, start=0, end=1):
  genders = []
  for n in names[int(len(names)*start):int(len(names)*end)]:
    genders.append(nc.smartClassify(n))
  c = Counter(genders)
  print '\n', start, end, c
  for g in c.keys():
    print '%s, %.2f' % (g, float(c[g]) / sum(c.values()))
  return c
 
ratio(names,0)
ratio(names,0, .1)
ratio(names,.1, .2)
ratio(names,.2, .3)
ratio(names,.3, .4)
ratio(names,.4, .5)
ratio(names,.5, .6)
ratio(names,.6, .7)
ratio(names,.7, .8)
ratio(names,.8, .9)
ratio(names,.9)
ratio(names,.95)
ratio(names,.96)
ratio(names,.97)
ratio(names,.98)
ratio(names,.99)

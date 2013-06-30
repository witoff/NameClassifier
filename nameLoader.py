import urllib
from zipfile import ZipFile
from os import listdir, path, remove
from datetime import datetime
import json

class NameLoader(object):

  def getNames(self):
    self.downloadNames()
    return self.parseNames()

  def downloadNames(self):
    if path.exists('names'):
      print 'name files already exist'
    else:
      print 'Downloading name files from Social Security Admin Website...'
      urllib.urlretrieve('http://www.ssa.gov/oact/babynames/names.zip', 'names.zip')
      print '--files downloaded'
      print 'Unzipping filies...'
      z = ZipFile('names.zip', 'r')
      z.extractall('names')
      print '--files unzipped'
      remove('names.zip')

  def parseNames(self, minAge=20, maxAge=70):
    if not path.exists('names.json'):
      print 'Names not already parsed.  Parsing now...'
      currentYear = datetime.now().year
      minYear = currentYear - maxAge
      maxYear = currentYear - minAge

      names = {}
      files = listdir('names')
      for name in files:
        if name[0:3] == 'yob' and \
          int(name[3:7]) > minYear and \
          int(name[3:7]) < maxYear:

          f = path.join('names', name)
          self.__parseFile(f, names)
      out = open('names.json', 'w')
      out.write(json.dumps(names))
      out.close()
    else:
      print 'Names already parsed.  Loading from names.json...'
      fName = open('names.json', 'r')
      names = json.loads(fName.read())
      fName.close()
    return names


  def __parseFile(self, path, names={}):
    f = open(path, 'r')
    for l in f.readlines():
        vals = l.split(',')
        name = vals[0].lower()
        if name not in names:
          names[name] = {'M':0, 'F':0}
        names[name][vals[1]] += int(vals[2])
    return names

if __name__ == '__main__':
  nl = NameLoader()
  print nl.getNames()
            

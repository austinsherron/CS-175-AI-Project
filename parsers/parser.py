import re
import sys

def isValid(ch):
  return re.match('^[a-z0-9]$', ch)


def fixArticle(inputString):
  inputString = inputString.lower()
  new_str = ''
  wasSpace = False
  for ch in inputString:
    if isValid(ch):
      new_str = new_str + ch
      wasSpace = False
    else:
      if not wasSpace:
        new_str = new_str + ','
        wasSpace = True
  return new_str

lns = []
with open(sys.argv[1], 'r') as f:
  lines = f.readlines()
  for line in lines:
    lns.append(fixArticle(line) + '\n')

with open(sys.argv[2], 'w') as f:
  f.writelines(lns)



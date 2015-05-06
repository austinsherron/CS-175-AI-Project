import csv
import sys
import re

def format_headline(headline):
  new_headline = ''
  has_space = False
  for ch in headline.lower():
    if re.match('[a-z0-9]', ch):
      new_headline += ch
      has_space = False
    else:
      if not has_space:
        new_headline += ' '
      has_space = True
  return new_headline.strip()

rows = []
with open(sys.argv[1], 'r') as f:
  reader = csv.reader(f, delimiter=',', quotechar='|')
  for row in reader:
    l = len(row)
    if row[l - 1] == 'none':
      continue
    headline = format_headline(''.join(row[0:l-1]))
    classification = 0
    v = float(row[l - 1])
    if v > 0:
      classification = 1
    elif v < 0:
      classification = -1
    rows.append([
      headline,
      row[l - 1],
      classification
    ])

with open(sys.argv[2], 'w') as f:
  writer = csv.writer(f) 
  for row in rows:
    writer.writerow(row)

  

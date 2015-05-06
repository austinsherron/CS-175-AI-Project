import csv
import sys
import re

def format_word(word):
  new_word = ''
  has_space = False
  for ch in word.lower():
    if re.match('[a-z0-9]', ch):
      new_word += ch
  return new_word.strip()

stop_words = {}
dictionary = {}
sorted_values = []
rows = []

with open(sys.argv[1], 'r') as f:
  for line in f:
    stop_words[format_word(line.strip())] = 1

with open(sys.argv[2], 'r') as f:
  reader = csv.reader(f, delimiter=',', quotechar='"')
  for row in reader:
    rows.append(row)
    for word in row[0].split(' '):
      w = word.strip()
      if not w in stop_words:
        if w in dictionary:
          dictionary[w] += 1
        else:
          dictionary[w] = 1

for (key, value) in dictionary.iteritems():
  sorted_values.append({
    'key': key,
    'value': value
  })

def sort_by_value(item):
  return item['value']

sorted_values = sorted(sorted_values, key=sort_by_value, reverse=True)

for i in range(200):
  print sorted_values[i]

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
dictionary_score = {}
sorted_values = []
rows = []

with open(sys.argv[1], 'r') as f:
  for line in f:
    stop_words[format_word(line.strip())] = 1

with open(sys.argv[2], 'r') as f:
  reader = csv.reader(f, delimiter=',', quotechar='"')
  for row in reader:
    rows.append(row)
    words = row[0].split(' ')
    score = float(row[1])
    if score > .001:
      score = 1
    elif score < -.001:
      score = -1
    else:
      score = 0
    for word in words:
      w = word.strip()
      if not w in stop_words:
        if w in dictionary_score:
          dictionary_score[w] += 1#score
        else:
          dictionary_score[w] = 1#score

for (key, value) in dictionary_score.iteritems():
  sorted_values.append({
    'key': key,
    'value': value
  })

def sort_by_value(item):
  return item['value']

sorted_values_good = sorted(sorted_values, key=sort_by_value, reverse=True)
sorted_values_bad = sorted(sorted_values, key=sort_by_value)

main_words = []
for i in range(15000):
  main_words.append(sorted_values_good[i]['key'])

'''for i in range(5000):
  main_words.append(sorted_values_bad[i]['key'])'''

with open('feature_words.txt', 'w') as f:
  for word in main_words:
    f.write(word + '\n')


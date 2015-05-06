import csv
import sys

mp = {}
wordArr = []

with open(sys.argv[1], 'r') as f:
  reader = csv.reader(f, delimiter=',', quotechar='"')
  for row in reader:
    name = row[0]
    score = row[2]
    if score == 'Category':
      continue
    cnt = int(row[3])
    tot = int(row[4])
    scores = [0, 0, 0, 0, 0, 0]
    if score in ['1', '2']:
      scores = [cnt, tot, 0, 0, 0, 0]
    elif score in ['5', '6']:
      scores = [0, 0, cnt, tot, 0, 0]
    elif score in ['9', '10']:
      scores = [0, 0, 0, 0, cnt, tot]
    else:
      continue
    if name not in mp:
      mp[name] = scores
    else:
      for i in range(0, len(scores)):
        mp[name][i] += scores[i]

for key in mp:
  value = mp[key]
  if float(value[0]) == 0:
    badFreq = 0
  else:
    badFreq = float(value[0]) / float(value[1])
  
  if float(value[2]) == 0:
    nullFreq = 0
  else:
    nullFreq = float(value[2]) / float(value[3])

  if float(value[4]) == 0:
    goodFreq = 0
  else:
    goodFreq = float(value[4]) / float(value[5])
  score = 1
  freq = badFreq
  if nullFreq >= goodFreq and nullFreq >= badFreq:
    score = 2
    freq = nullFreq
  elif goodFreq >= goodFreq and goodFreq >= badFreq:
    score = 3
    freq = goodFreq
  wordArr.append({
    'word': key,
    'score': score,
    'freq': freq
  })

wordArr.sort(key=lambda x: x['freq'], reverse=True)
f = open('data/imdb-parsed.csv', 'w')
f.write('Word,Score\n')
for line in wordArr:
  f.write(line['word'] + ',' + str(line['score']) + '\n')
f.close()





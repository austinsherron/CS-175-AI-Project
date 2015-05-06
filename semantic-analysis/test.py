import csv
import sys
from collections import defaultdict


word_ratings = defaultdict(set)
words = []

with open(sys.argv[1]) as f:
	reader = csv.reader(f)
	for row in reader:
		word_ratings[row[0]].add(row[1])
		words.append(row[1])

duplicates = set()
for word in words:
	if word in word_ratings['neg'] and word in word_ratings['pos']:
		duplicates.add(word)

#with open(sys.argv[2], 'w') as f:
#	writer = csv.writer(f)
#	for word in sorted(duplicates):
#		good_sum = len([w for w in word_ratings['pos'] if w == word])
#		bad_sum = len([w for w in word_ratings['neg'] if w == word])
#		writer.writerow([word, good_sum, bad_sum])

with open(sys.argv[2], 'w') as f:
	writer = csv.writer(f)
	for word in word_ratings['pos']:
		writer.writerow(['pos', word])
	for word in word_ratings['neg']:
		writer.writerow(['neg', word])

#for word in sorted(duplicates):
#	good_sum = len([w for w in word_ratings['pos'] if w == word])
#	bad_sum = len([w for w in word_ratings['neg'] if w == word])
#
#
#	try:
#		if good_sum > bad_sum + 5:
#			word_ratings['neg'].remove(word)
#		elif bad_sum + 5 > good_sum:
#			word_ratings['pos'].remove(word)
#	except ValueError:
#		pass
#
#with open(sys.argv[2], 'w') as f:
#	writer = csv.writer(f)
#	for word in word_ratings['pos']:
#		writer.writerow(['pos', word])
#	for word in word_ratings['neg']:
#		writer.writerow(['neg', word])
#		

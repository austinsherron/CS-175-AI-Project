import csv
import sys


with open(sys.argv[1]) as f:
	pass

with open(sys.argv[2], 'w') as f:
	writer = csv.writer(f)
	for word,cat in words.items():
		if '#' in word:
			word = word[:word.find('#')]
		row = [word,cat]
		writer.writerow(row)

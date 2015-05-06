import csv
import sys

symbols = set()

with open('nasdaqlisted.txt') as f:
	for line in f:
		line = line.strip().split('|')
		if line[0] == 'Y':
			if '$' not in line[1] and len(line[1]) == 4:
				symbols.add(line[1].strip())

with open('symbols.csv', 'w') as f:
	writer = csv.writer(f)
	for sym in symbols:
		writer.writerow([sym])
	

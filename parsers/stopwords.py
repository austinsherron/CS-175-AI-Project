import csv
import sys


def build_stopwords_set(file):
	stopwords = set()
	with open(file) as f:
		reader = csv.reader(f)
		for line in reader:
			stopwords.add(str(line[0]))
	return stopwords


def remove_stopwords(in_file, out_file, stopwords):
	new_lines = []
	with open(in_file) as in_f:
		reader = csv.reader(in_f)
		for line in reader:
			new_line = []
			for word in line:
				if word not in stopwords:
					new_line.append(word)
			new_lines.append(new_line)

	with open(out_file, 'w') as out_f:
		writer = csv.writer(out_f)
		writer.writerows(new_lines)


if __name__ == '__main__':
	stopwords = build_stopwords_set('stopwords.txt')
	remove_stopwords(sys.argv[1], sys.argv[2], stopwords)

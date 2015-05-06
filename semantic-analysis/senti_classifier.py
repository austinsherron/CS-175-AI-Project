#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

import csv
import nltk.classify.util
import sys
from collections import defaultdict
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import sentiwordnet as swn
 

def build_words(file):
	words = defaultdict(int)
	with open(file) as f:
		reader = csv.reader(f)
		for row in reader:
			words[row[1]] += -1 if row[0][0] == 'n' else 1
	return words


def custom_in(arg, structure):
	if arg in structure:
		return arg 
	elif arg.strip('ed') in structure:
		return arg.strip('ed')
	elif arg.strip('ing') in structure:
		return arg.strip('ing')
	elif arg.strip('es') in structure:
		return arg.strip('es')
	elif arg.strip('ers') in structure:
		return arg.strip('ers')
	elif arg.strip('s') in structure:
		return arg.strip('s')


def score_headlines(words, file):
	scored_headlines = []
	with open(file) as f:
		reader = csv.reader(f)
		for headline in reader:
			score = 0
			word_scores = {}
			for word in headline:
				actual_word = custom_in(word, words)
				if actual_word:
					score += words[actual_word]
#					word_scores[word] = words[actual_word]
#				else:
#					word_scores[word] = 0
			scored_headlines.append([' '.join(headline), score])
	return scored_headlines


def build_output_csv(scored_headlines, file):
	with open(file, 'w') as f:
		writer = csv.writer(f)
		for headline in scored_headlines:
			writer.writerow([headline[0], headline[1]])


if __name__ == '__main__':
	words = build_words(sys.argv[1])
	scored_headlines = score_headlines(words, sys.argv[2])
	build_output_csv(scored_headlines, sys.argv[3])


	

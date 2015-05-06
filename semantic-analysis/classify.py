#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

import csv
import sys
from nltk.classify import NaiveBayesClassifier


def get_all_words(file):
	all_words = []
	with open(file) as f:
		reader = csv.reader(f)
		for row in reader:
			pass
		

if __name__ == '__main__':

	pass

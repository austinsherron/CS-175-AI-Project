#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

import csv
import sys
from collections import defaultdict


def get_stopwords(file):
	stopwords = set()
	with open(file) as f:
		reader = csv.reader(f)
		for row in reader:
			stopwords.add(row[0])
	return stopwords


def get_cat_from_score(score):
	score = int(score)
	if score > 0:
		return 1
	elif score < 0:
		return -1
	return score


def parse_scored_headlines_from_csv(file):
	categories = defaultdict(list)
	with open(file) as f:
		reader = csv.reader(f)
		for row in reader:
			words = row[0].split(' ')
			cat = get_cat_from_score(row[1])
			for word in words:
					categories[cat].append(word)
	return dict(categories)


def remove_stopwords(cat_dict, stopwords):
	new_cat_dict = defaultdict(list)
	for cat in cat_dict:
		for word in cat_dict[cat]:
			if word not in stopwords:
				new_cat_dict[cat].append(word)
	return new_cat_dict


def dict_to_word_score_pairs(cat_dict):
	word_score_pairs = []
	for cat in cat_dict:
		for word in cat_dict[cat]:
			word_score_pairs.append([word, cat])
	return word_score_pairs


def total_in_cat(cat, cat_dict):
	return len(cat_dict[cat])


def count_word_in_cat(word, cat, cat_dict):
	words = [w for w in cat_dict[cat] if w == word]
	return len(words)


def build_row(row, cat_dict):
	word = row[0]
	cat = row[1]
	count = count_word_in_cat(word, cat, cat_dict)
	total  = total_in_cat(cat, cat_dict)
	rel_freq = float(count / total)
	return [word, cat, count, total, rel_freq]


def build_word_rel_freq_dict(cat_dict, word_score_pairs):
	rel_freq_dict = defaultdict(float)
	total = len(word_score_pairs)
	for i, row in enumerate(word_score_pairs):
		word_info = build_row(row, cat_dict)
		rel_freq_dict[word_info[0]] += word_info[4]
	return dict(rel_freq_dict)


if __name__ == '__main__':

	cat_dict = parse_scored_headlines_from_csv('headlines-scored-w-custom-lex.csv')
	stopwords = get_stopwords('../data/stopwords.csv')
	no_stopwords_cat_dict = remove_stopwords(cat_dict, stopwords)

	word_score_pairs = dict_to_word_score_pairs(cat_dict)
	word_freqs = build_word_rel_freq_dict(cat_dict, word_score_pairs)


	with open(sys.argv[2]) as f:
		writer = csv.writer(f)
		for pair in word_score_pairs:
			row = build_row(pair, cat_dict)
			row += [row[4] / word_freqs[row[0]]]
			writer.writerow(row)

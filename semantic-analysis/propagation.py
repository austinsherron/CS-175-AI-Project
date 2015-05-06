#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

################################################################################
## IMPORTS #####################################################################
################################################################################


import csv
import os
import sys
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn


################################################################################
################################################################################
################################################################################


################################################################################
## WORDNET METHODS #############################################################
################################################################################


def wordnet_sense_propagation(synsets_list: '[[synsets]]', i: int, methods: '{methods}', remove_overlap=True):
	output = [[synset] for synset in synsets_list]			# initialize ouput matrix of synsets
	for i in range(i):						  				# propagate for i iterations
		new = {}
		for j in range(len(synsets_list)):
			same = find_same(output[j][i])					# find synsets related to current synset
			others = get_other_synsets(output, i, j)		# get the union of synsets other than the one being considered
			diff = find_diff(others)						# find synsets in opposition to other synsets
			new[j] = merge_dicts(same, diff)				# add them to a dictionary whose keys are indexes of currently considered synsets
		for j in range(len(synsets_list)):
			output[j].append(list(new[j].values()))			# add findings to corresponding synsets list
	return output


def find_same(synsets: '[synset]') -> '{str: synset}':
	new = {}
	for syn in synsets:				
		new[syn.name()] = syn
		for related in syn.also_sees():
			new[related.name()] = related
		for related in syn.similar_tos():
			new[related.name()] = related
		for lemma in syn.lemmas():
			for related in lemma.pertainyms():
				new[related.name()] = related.synset()
			for related in lemma.derivationally_related_forms():
				new[related.name()] = related.synset()
	return new


def find_diff(synsets: '[synset]') -> '{str: synset}':
	new = {}
	for syn in synsets:
		for lemma in syn.lemmas():
			for related in lemma.antonyms():
				new[related.name()] = related.synset()
	return new


################################################################################
################################################################################
################################################################################
	

################################################################################
## HELPERS #####################################################################
################################################################################


def create_seeds(words: [str], part_of_speech=None) -> '[synsets]':
	synsets = []
	for word in words:
		if part_of_speech:
			synsets += (wn.synsets(word, part_of_speech))
		else:
			synsets += (wn.synsets(word))
	return synsets


def print_by_line(iterable) -> None:
	for item in iterable:
		print(item)


def get_other_synsets(synsets_list: '[[synset]]', i: int, j: int) -> '[synset]':
	others = []
	for k in range(len(synsets_list)):
		if j != k:
			for synset in synsets_list[k][i]:
				others.append(synset)
	return others


def merge_dicts(dict1: dict, dict2: dict) -> dict:
	merged = dict1.copy()
	merged.update(dict2)
	return merged


def subtract_dicts(dict1: dict, dict2: dict) -> dict:
	subtracted = {}
	for k,v in dict1.items():
		if k not in dict2:
			subtracted[k] = v
	return subtracted


def build_seeds(in_file):
	pos_seeds = []
	neg_seeds = []
	with open(in_file) as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == 'pos':
				pos_seeds.append(row[1])
			elif row[0] == 'neg':
				neg_seeds.append(row[1])
	return (pos_seeds, neg_seeds)


def build_output_csv(out_file, output):
	with open(out_file, 'w') as f:
		writer = csv.writer(f)
		for i, seq in enumerate(output):
			tag = 'pos' if i == 0 else 'neg'
			for syn in sorted(seq[-1]):
				word = syn.name()
				writer.writerow([tag, word[:word.find('.')]])


################################################################################
################################################################################
################################################################################


################################################################################
## MAIN ########################################################################
################################################################################


if __name__ == '__main__':

	# seed words determine type of lexicon
#	positive_words = ["good", "excellent"]	# , "nice", "positive", "fortunate", "correct", "superior"]
#	negative_words = ["bad","terrible"]		#, "poor", "negative", "unfortunate", "wrong", "inferior"]

	try:
		seeds_word_tuple = build_seeds(sys.argv[1])
	except IndexError:
		print("error: please supply a path to a csv with seeds words")
		sys.exit(1)

	pos_synsets = create_seeds(seeds_word_tuple[0]) 
	neg_synsets = create_seeds(seeds_word_tuple[1]) 

#	pos_synsets = create_seeds(['rise', 'grow', 'upgrade', 'upward']) 
#	neg_synsets = create_seeds(['fall', 'tumble', 'shrink', 'downgrade', 'downtrend']) 

	all_synsets = [pos_synsets, neg_synsets]
	# number of propagation iterations: more leads to larger, less consistent lexicons
	it = 3									

	output = wordnet_sense_propagation(all_synsets, it, None)

	build_output_csv(sys.argv[2], output)
	
	for i, seq in enumerate(output):
		print("<synsets n={0} iteration={1}>".format(i+1, it))
		for synset in sorted(seq[-1]):
			print("\t" + synset.name())
		print("</synsets>\n")


################################################################################
################################################################################
################################################################################

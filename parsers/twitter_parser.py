import csv
import sys
from collections import defaultdict


def parse_tweet(tweet):
	new_tweet = []
	tweet = tweet.strip().split(' ')
	for word in tweet:
		if word != '' and word[0] != '@':
			new_tweet.append(word)
	return new_tweet


def parse_tweets(file):
	tweets = defaultdict(list)
	with open(file) as f:
		reader = csv.reader(f)
		for row in reader:
			tweets[row[0]].append(parse_tweet(row[-1]))
	return tweets


if __name__ == '__main__':
	print(parse_tweets(sys.argv[1]))

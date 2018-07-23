from collections import Counter
import numpy as np
import random as random
import nltk
from nltk import word_tokenize
from nltk.util import ngrams

"""Model functions (adapted from Sweta and Elle)""" 
def basic_markov_model(filename, wordnum, seed_var=None):
	random_max = 2**32 - 1
	if not seed_var:
		random.seed(None)
		startseed = random.randint(0, random_max)
	else:
		startseed = seed_var

	# set my seed
	random.seed(startseed)

	with open(filename, encoding = 'utf-8') as f:
		corpus = f.read()

	# Some light cleaning    
	corpus = corpus.lower()
	corpus.replace('\n',';')

	# Get two grams, three grams, four grams
	token = word_tokenize(corpus)
	trigrams = list(ngrams(token,3))

	###### 3 grams ###############
	start_gram = random.choice(trigrams) # random starting value
	start1 = start_gram[0]
	start2 = start_gram[1]

	model_text = [start1, start2]
	for i in range(0,wordnum):
		cumsum = []
		gram_choices = []
		# Find all elements in the trigram corpus that start with startword
		choices = [i for i, j in enumerate(trigrams) if j[0]==start1 and j[1] == start2]
		# Get all the trigrams that occur
		newlist = [trigrams[i] for i in choices]
		# Get the most popular one
		d2 = Counter(newlist)
		# Get the cumulative probabilities of
		for k,v in d2.items():
			cumsum.append(v)
			gram_choices.append(k)
		cumsum = np.array([x / sum(cumsum) for x in cumsum])
		cumsum = np.cumsum(cumsum)
		# Generate a random number
		r = random.random()
		ind = np.min(np.where(cumsum > r))
		# Get the most common n-gram from this model 
		new_word = gram_choices[ind][2]
		start1 = start2
		start2 = new_word
		model_text.append(new_word)

	out_str = ' '.join(model_text)
	out_str =out_str.replace('break', '\n\n')
	out_str = "\n\n" + out_str + "\n\n"
	return out_str, startseed

def format_output(txt, startseed):
	import re
	import textwrap as tw

	txt_fmt = tw.fill(txt, 75)
	txt_fmt = re.sub(r'([?!.)}]{0,2}\s?)([a-z\s]{,}\s?\#?\s?[0-9+&]{,}\s?:)', r'\n\n\2\n', txt_fmt)
	txt_fmt = "TAUNT # %d\n\n\n" %startseed + txt_fmt

	return txt_fmt


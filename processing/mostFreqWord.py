# Uses tfidf to calculate important named entites (This intersected with NEs.py will remove redundant named entities)
from __future__ import print_function
import nltk
import re, pprint
from nltk.corpus import stopwords

from nltk.book import *
from nltk.corpus import PlaintextCorpusReader

text_raw = open("ofk.txt").read()
tokens = nltk.word_tokenize(text_raw)
tokens = [re.sub('\.','',w) for w in tokens] #remove periods
tokens = [w for w in tokens if w.isalpha()] #just keep words
tokens_freq = FreqDist(tokens)
mostFreq = 0
mostFWord = ""
for tok in tokens:
	if tokens_freq[tok] > mostFreq:
		mostFreq = tokens_freq[tok]
		mostFWord = tok
print (str(mostFreq) + " : " + mostFWord)
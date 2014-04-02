# This program finds the intersection of the two sets for named entities calcuated from NEs.py and tfidf.py
from __future__ import print_function
import nltk
from numpy import loadtxt
from sets import Set

NEs = open("NEs/NEs.txt").read().split('\n')
tfidf = open("tfidf/tfidf.txt").read().split('\n')
final = Set(NEs).intersection(Set(tfidf)) - Set([''])
log = open("finalNEs/finalNEs.txt", "w") 
for x in final:
	print(x, file=log)

# Uses tfidf to calculate important named entites (This intersected with NEs.py will remove redundant named entities)
from __future__ import division
from __future__ import print_function
from math import log
from math import exp
import nltk
import json
import re, pprint
from nltk.corpus import stopwords

from nltk.book import *
from nltk.corpus import PlaintextCorpusReader

text1 = FreqDist(text1)
text2 = FreqDist(text2)
text3 = FreqDist(text3)
text4 = FreqDist(text4)
text5 = FreqDist(text5)
text6 = FreqDist(text6)
text7 = FreqDist(text7)
text8 = FreqDist(text8)
text9 = FreqDist(text9)
def importance(w, tokens_freq, tokens_10, text1, text2, text3, text4, text5, text6, text7, text8, text9):
	tf = 0.5 + (0.5 * tokens_freq[w])/(max(tokens_freq[w] for w in tokens_10))
	iter = 0
	if text1[w] > 0:
		iter+=1
	if text2[w] > 0:
		iter+=1
	if text3[w] > 0:
		iter+=1
	if text4[w] > 0:
		iter+=1
	if text5[w] > 0:
		iter+=1
	if text6[w] > 0:
		iter+=1
	if text7[w] > 0:
		iter+=1
	if text8[w] > 0:
		iter+=1
	if text9[w] > 0:
		iter+=1
	if(iter == 0):
		iter = exp(-320)
	idf = log(9/iter)
	return tf * idf
# select chapter to print, chapter 0 for whole book
chapter = 2
# for chapter in range(1,5):
if(chapter == 0):
	text_raw = open("ofk.txt").read()
else:
	text_raw = open("ofk_ch" + str(chapter) + ".txt").read()
tokens = nltk.word_tokenize(text_raw)
tokens = [re.sub('\.','',w) for w in tokens] #remove periods
tokens = [w for w in tokens if w.isalpha()] #just keep words
# tokens = [w for w in tokens if not w in stopwords.words('english')]
tokens = [w for w in tokens if len(w) > 1]
tokens_freq = FreqDist(tokens)
tokens_10 = [w for w in tokens if tokens_freq[w] > 30]
tokens_freq = FreqDist(tokens_10)

tokens_table = [dict(name = w, value=importance(w, tokens_freq, tokens_10, text1, text2, text3, text4, text5, text6, text7, text8, text9)) for w in tokens_freq]
a = lambda e1, e2: int(1000000*(e1['value'] - e2['value']))

sorted_table = sorted(tokens_table, cmp = a, reverse=True)
nums = 50
final_table = sorted_table[:nums];
if(chapter == 0):
	log = open("tfidf/tfidf.txt", "w")
else:
	log = open("tfidf/tfidf_ch" + str(chapter) + ".txt", "w")
for x in final_table:
	print(x["name"], file=log)

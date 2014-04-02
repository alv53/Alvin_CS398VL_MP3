# This program takes the finalNEs.txts and calculates when two named entities are in the same sentence. This essentially pairs them together and will allow our edge bundler to link the two nodes.
# The implementation for the tf-idf takes a VERY VERY VERY VERY LONG time to run, because I chose possibly the slowest and longest and redundant method possible. However it wasn't until much later that I realized this. 
# It would have been much better to save the importance of every word in the book then just pull out that value as I needed it.
# This took 33175 seconds to run or 9 hours
from __future__ import division
from __future__ import print_function
from math import log

import nltk
import json

import re, pprint
from sets import Set

from nltk.corpus import stopwords
from nltk.book import *
from nltk.corpus import PlaintextCorpusReader

def network(chapter):
	if(chapter == 0):
		NEs = open("finalNEs/finalNEs.txt").read().split('\n')
		text_raw = open("ofk.txt").read()
	else:
		NEs = open("finalNEs/finalNEs_ch" + str(chapter) + ".txt").read().split('\n')
		text_raw = open("ofk_ch" + str(chapter) + ".txt").read()
	result = [dict(name="", relations=[""])]
	for NE in NEs:
		result.append(dict(name=NE, relations=[""]))

	# The next line is needed because of the extra blank list elements at the beginning and end (Beginning I added, end added from newlines in finalNEs.txt)
	result = result[1:len(result)-1]
	corpus = PlaintextCorpusReader('.', 'ofk\.txt')
	sentences = corpus.sents()
	for x in range(len(sentences)):
		for NEdict in result:
			if NEdict["name"] in sentences[x]:
	# 			# We are in a sentence with a named entity
				for n in result:
					if n["name"] in sentences[x] and n["name"] != NEdict["name"]:
						NEdict["relations"].append(n["name"])
	for NEdict in result:
		NEdict["relations"] = Set(NEdict["relations"][1:])
	final = [dict(name=r["name"], imports=list(r["relations"]), url=r["name"]+".html") for r in result]
	for finals in final:
		with open("../webpage/" + finals["name"] + ".html", "w") as f1:
			with open("part1.html") as f:
				for line in f:
					f1.write(line)
				f1.write(finals["name"])
			with open("part2.html") as f:
				for line in f:
					f1.write(line)
				f1.write("\tmain(\"data/" + finals["name"] + ".json" + "\");\n</script>")

	with open("../webpage/data/edgeBundle.json",'w') as outfile:
		json.dump(final,outfile, sort_keys = True, indent = 4, ensure_ascii=False)
	# for elem in final:
	# 	result = [[dict(name="", children=[])]] 
	# 	for rel in range(len(elem["imports"])):
	# 		result.append(dict(name=elem["imports"][rel], children=tfidf(elem["name"], elem["imports"][rel], sentences)))
	# 		# result.append(dict(name=elem["imports"][rel], children=[dict(name="word", size=0.000012)] * 5))
	# 		print(str(rel) + " done")
	# 	root = dict(name=elem["name"], children=result[1:])
	# 	with open("../webpage/data/" + str(elem["name"]) + ".json",'w') as outfile:
	# 		json.dump(root,outfile, sort_keys = True, indent = 4, ensure_ascii=False)

def importance(word, sentences):
	# calculates the importance of a word with tfidf
	freqW = 0;
	occ = 0
	for sent in sentences:
		if word in sent:
			freqW = freqW+1
			if sent.count(word) > occ:
				occ = sent.count(word)
	# most frequent word is "the", which occurs 12663 times, calculated in mostFreqWord.py
	tf = 0.5 + (0.5 * occ)/12663
	idf = log(len(sentences)/freqW)
	return tf * idf


def tfidf(original, word, sentences):
	# print(original + " and " + word)
	sharedWords=set([])
	for sent in sentences:
		if original in sent and word in sent:
			# print("simil")
			for w in sent:
				if w != original and w != word:
					sharedWords.add(w)
	# Now we want to determine the most important of the shared words
	table = [dict(name = w, value=importance(w, sentences)) for w in sharedWords]
	a = lambda e1, e2: int(1000000*(e1['value'] - e2['value']))

	sorted_table = sorted(table, cmp = a, reverse=True)

	resList = list(sorted_table)[0:5]
	return [dict(name=resList[sW]["name"], size=resList[sW]["value"]) for sW in range(len(resList))]
network(0)
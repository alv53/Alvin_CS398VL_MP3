#This file finds the named entities in the entire book, as well as for each chapter. 
from __future__ import print_function
import nltk
from sets import Set
# The reason these outputs are being written to seperate files is because this program a total of 1254.4 seconds (or roughly 21 minutes to execute)
def extract_names(text):
    persons = Set([])
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'node') and chunk.node == 'PERSON':
                person = ' '.join(c[0] for c in chunk.leaves())
                index = text.find(person)
                persons.add(person)
    return persons

log = open("NEs/NEs.txt", "w") 
content = open("ofk.txt", 'r').read()
namedEntities = extract_names(content)
for NE in namedEntities:
	print(NE, file = log)


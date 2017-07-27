from io_utils import read_input, output_data
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
from spacy.en import English
from nltk import word_tokenize
import numpy as np
import string

lemmatizer = WordNetLemmatizer()

nlp = spacy.load('en')
parser = English()

exclude = set(string.punctuation)

from scraping import docu
# from query_processor import res

def sent_similarity(word_1, list_1, list_2):
	w1 = normalize(word_1)
	if(list_1 != ''):
		w2 = get_tokens(list_1)
	if(list_2 != ''):
		w2 = get_tokens(list_2)
	# if(list_3 != ''):
	# 	w2 = get_tokens(list_3)

	w2 = list(set(w2))

	score = 0
	count = 0
	for w in w1:
		s1 = wn.synsets(w)
		for elem in w2:
			s2 = wn.synsets(elem)
			if(len(s1) != 0 and len(s2) != 0):
				s = s1[0].wup_similarity(s2[0])
				if(s > 0):
					score += s
					count += 1

	if(count == 0): 
		return 0
	return (score/count)

	#return score





def normalize(sentence):
	stop_words=set(stopwords.words("english"))
	sentence = ''.join(ch for ch in sentence if ch not in exclude)

	sentence = sentence.decode('utf-8').strip()
	parsed = nlp(sentence)
	words = []
	
	for word in parsed:
		words.append(word.lemma_)

	words=[w for w in words if not w in stop_words]

	#print words
	return words

def get_tokens(collection):
	items = []

	if(collection != ''):
		for item in collection:
			var = item.split(' ')
			for i in var:
				i = lemmatizer.lemmatize(i)
				items.append(i)
	return items




def get_similarity(docu , question):
	temp_rank = 0
	temp_doc = ''
	for elem in docu:
		rank = sent_similarity(question, elem['subject'], elem['object'])
		if(rank > temp_rank):
			temp_rank = rank
			temp_doc = elem['text']

	print temp_doc


# word_1 = 'what is a wing'
# word_2 = 'The wing is an aerodynamic lifting surface that provides conventional lift and control for the spaceship.'

# print word_similarity(word_1, word_2)

# w1 = u'go'
# w2 = u'walk'
# s1 = wn.synsets(w1)
# s2 = wn.synsets(w2)

# # #score
# print s1[0].wup_similarity(s2[0])

question = 'what are engine limitations  '
get_similarity(docu,question)

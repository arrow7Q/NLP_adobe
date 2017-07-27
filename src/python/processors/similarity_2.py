import os
import pandas as pd
import nltk
import gensim
from gensim import corpora, models, similarities
from scraping import docu

import numpy as np
import math
from scipy.spatial import distance

from random import sample
import sys
from nltk.corpus import stopwords

def get_tokens(collection):
	items = []

	if(collection != ''):
		for item in collection:
			var = item.split(' ')
			for i in var:
				items.append(i)
	return items

documents = []
for elem in docu:
	#documents.append(nltk.word_tokenize(elem['text'].decode('utf-8')))
	var = get_tokens(elem['subject'])
	var = get_tokens(elem['object'])
	var = get_tokens(elem['SVO'])
	Var = list(set(var))
	documents.append(Var)



model = gensim.models.Word2Vec(documents, min_count=1, size = 100)

model.save('testmodel')
model = gensim.models.Word2Vec.load('testmodel')



#---similarity
class PhraseVector:
	def __init__(self, phrase):
		self.vector = self.PhraseToVec(phrase)
	# <summary> Calculates similarity between two sets of vectors based on the averages of the sets.</summary>
	# <param>name = "vectorSet" description = "An array of arrays that needs to be condensed into a single array (vector). In this class, used to convert word vecs to phrases."</param>
	# <param>name = "ignore" description = "The vectors within the set that need to be ignored. If this is an empty list, nothing is ignored. In this class, this would be stop words."</param>
	# <returns> The condensed single vector that has the same dimensionality as the other vectors within the vecotSet.</returns>
	def ConvertVectorSetToVecAverageBased(self, vectorSet, ignore = []):
		if len(ignore) == 0: 
			return np.mean(vectorSet, axis = 0)
		else: 
			return np.dot(np.transpose(vectorSet),ignore)/sum(ignore)

	def PhraseToVec(self, phrase):
		cachedStopWords = stopwords.words("english")
		phrase = phrase.lower()
		wordsInPhrase = [word for word in phrase.split() if word not in cachedStopWords]
		vectorSet = []
		for aWord in wordsInPhrase:
			try:
				wordVector=model[aWord]
				vectorSet.append(wordVector)
			except:
				pass
		return self.ConvertVectorSetToVecAverageBased(vectorSet)

	# <summary> Calculates Cosine similarity between two phrase vectors.</summary>
	# <param> name = "otherPhraseVec" description = "The other vector relative to which similarity is to be calculated."</param>
	def CosineSimilarity(self, otherPhraseVec):
		cosine_similarity = np.dot(self.vector, otherPhraseVec) / (np.linalg.norm(self.vector) * np.linalg.norm(otherPhraseVec))
		try:
			if math.isnan(cosine_similarity):
				cosine_similarity=0
		except:
			cosine_similarity=0		
		return cosine_similarity


if __name__ == "__main__":

	print "###################################################################"
	
	userInput1 = 'what is the structure of concept topic'
	phraseVector1 = PhraseVector(userInput1)
	#userInput2 = raw_input("Type the phrase2: ")

	rank = 0
	temp_doc = ''

	for elem in docu:

		phraseVector2 = PhraseVector( elem['text'] )
		simi = phraseVector1.CosineSimilarity(phraseVector2.vector)
		if(simi > rank):
			rank =simi
			temp_doc = elem['text']


	print "###################################################################"
	print 'asnwer :', temp_doc
	print 'score :', rank



#df=pd.read_csv('jokes.csv');



#x=df['Question'].values.tolist()
#y=df['Answer'].values.tolist()

#corpus= x+y

#tok_corp= [nltk.word_tokenize(sent.decode('utf-8')) for sent in corpus]
#print tok_corp[:20]
           
#model = gensim.models.Word2Vec(tok_corp, min_count=1, size = 32)

#model.save('testmodel')
#model = gensim.models.Word2Vec.load('test_model')
#print model.most_similar('mom')
#model.most_similar([vector])



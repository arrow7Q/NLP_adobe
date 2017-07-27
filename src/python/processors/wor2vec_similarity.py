import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

######################
# Loading word2vec
######################
import gensim
from scraping import docu
from gensim.models import word2vec
from io_utils import read_input
# Change this to your own path.
pathToBinVectors = '/Users/utkarsh/Documents/nlp/model/GoogleNews-vectors-negative300.bin'

print "Loading the data file... Please wait..."
model1 = gensim.models.KeyedVectors.load_word2vec_format(pathToBinVectors, binary=True, limit=200000)
print "Successfully loaded 3.6 G bin file!"

# How to call one word vector?
# model1['resume'] -> This will return NumPy vector of the word "resume".

import numpy as np
import math
from scipy.spatial import distance

from random import sample
import sys
from nltk.corpus import stopwords


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
				wordVector=model1[aWord]
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



	userInput1 = read_input()
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


	
	# phraseVector2 = PhraseVector(userInput2)
	# similarityScore  = phraseVector1.CosineSimilarity(phraseVector2.vector)

	# print "###################################################################"
	# print "Similarity Score: ", similarityScore
	# print "###################################################################"
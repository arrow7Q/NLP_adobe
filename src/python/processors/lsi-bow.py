from scraping import docu
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint  # pretty-printer
from nltk.corpus import stopwords

stoplist=set(stopwords.words("english"))


documents = []
for elem in docu:
	documents.append(elem['text'])

# remove common words and tokenize
#stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
			for document in documents]

# remove words that appear only once 

frequency = defaultdict(int)
for text in texts:
	for token in text:
		frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
			for text in texts]


#pprint(texts)

dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict')  
#print(dictionary)

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus)  
#print(corpus)

#transforming model
# if (os.path.exists("/tmp/deerwester.dict")):
# 	dictionary = corpora.Dictionary.load('/tmp/deerwester.dict')
# 	corpus = corpora.MmCorpus('/tmp/deerwester.mm')

tfidf = models.TfidfModel(corpus)

# doc_bow = [(0, 1), (1, 1)]
# print(tfidf[doc_bow]) # step 2 -- use the model to transform vectors

corpus_tfidf = tfidf[corpus]
#for doc in corpus_tfidf:
	#print(doc)

#we can also use this lsi model
lsi = models.LsiModel(corpus_tfidf, id2word = dictionary, num_topics=2) 
corpus_lsi = lsi[corpus_tfidf] 

# lsi.print_topics(2)

lsi_test = models.LsiModel(corpus, id2word = dictionary, num_topics=2)

index = similarities.MatrixSimilarity(lsi[corpus_tfidf]) 

index.save('/tmp/deerwester.index')
index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')


#user queries

doc = " how can wheels avoid slipping "
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] 
#print(vec_lsi)

sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
#print (sims)
print documents[sims[0][0]]

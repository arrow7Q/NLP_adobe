Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 12:39:47) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "copyright", "credits" or "license()" for more information.
>>> WARNING: The version of Tcl/Tk (8.5.9) in use may be unstable.
Visit http://www.python.org/download/mac/tcltk/ for current information.

>>> import nltk
>>> from nltk.corpus import stopwords
>>> stop_words=set(stopwords.words("english"))
>>> print stiop_words

Traceback (most recent call last):
  File "<pyshell#4>", line 1, in <module>
    print stiop_words
NameError: name 'stiop_words' is not defined
>>> print stop_words
set([u'all', u'just', u'being', u'over', u'both', u'through', u'yourselves', u'its', u'before', u'o', u'hadn', u'herself', u'll', u'had', u'should', u'to', u'only', u'won', u'under', u'ours', u'has', u'do', u'them', u'his', u'very', u'they', u'not', u'during', u'now', u'him', u'nor', u'd', u'did', u'didn', u'this', u'she', u'each', u'further', u'where', u'few', u'because', u'doing', u'some', u'hasn', u'are', u'our', u'ourselves', u'out', u'what', u'for', u'while', u're', u'does', u'above', u'between', u'mustn', u't', u'be', u'we', u'who', u'were', u'here', u'shouldn', u'hers', u'by', u'on', u'about', u'couldn', u'of', u'against', u's', u'isn', u'or', u'own', u'into', u'yourself', u'down', u'mightn', u'wasn', u'your', u'from', u'her', u'their', u'aren', u'there', u'been', u'whom', u'too', u'wouldn', u'themselves', u'weren', u'was', u'until', u'more', u'himself', u'that', u'but', u'don', u'with', u'than', u'those', u'he', u'me', u'myself', u'ma', u'these', u'up', u'will', u'below', u'ain', u'can', u'theirs', u'my', u'and', u've', u'then', u'is', u'am', u'it', u'doesn', u'an', u'as', u'itself', u'at', u'have', u'in', u'any', u'if', u'again', u'no', u'when', u'same', u'how', u'other', u'which', u'you', u'shan', u'needn', u'haven', u'after', u'most', u'such', u'why', u'a', u'off', u'i', u'm', u'yours', u'so', u'y', u'the', u'having', u'once'])
>>> from nltk import word_tokenize ,sent_tokenize
>>> example="this is th best day of my life.Havent been happier before"
'
>>> words=word_tokenize(example)
>>> print words
['this', 'is', 'th', 'best', 'day', 'of', 'my', 'life.Havent', 'been', 'happier', 'before']
>>> filtered_sentence=[w for w in words if not w in stop_words]
\
>>> print filtered_sentence
['th', 'best', 'day', 'life.Havent', 'happier']
>>> 
>>> #pos tagging part
>>> tagged= nltk.pos_tag(words)
>>> print tagged
[('this', 'DT'), ('is', 'VBZ'), ('th', 'JJ'), ('best', 'RBS'), ('day', 'NN'), ('of', 'IN'), ('my', 'PRP$'), ('life.Havent', 'NN'), ('been', 'VBN'), ('happier', 'JJR'), ('before', 'IN')]
>>> namedent = nltk.ne_chunk(tagged)
>>> print namedent
(S
  this/DT
  is/VBZ
  th/JJ
  best/RBS
  day/NN
  of/IN
  my/PRP$
  life.Havent/NN
  been/VBN
  happier/JJR
  before/IN)
]
>>> namedent.draw()
>>> namedent = nltk.ne_chunk(tagged,binary=True)
>>> namedent.draw()
>>> print namedent
(S
  this/DT
  is/VBZ
  th/JJ
  best/RBS
  day/NN
  of/IN
  my/PRP$
  life.Havent/NN
  been/VBN
  happier/JJR
  before/IN)
>>> print nltk.__file__
/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/nltk/__init__.pyc
>>> 

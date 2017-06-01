import sys
import nltk
from nltk import word_tokenize, sent_tokenize ,pos_tag ,ne_chunk
from nltk.corpus import stopwords

ques=sys.stdin.readline()

words= word_tokenize(ques)
tagged=pos_tag(words)
namedent=ne_chunk(tagged)

print namedent

namedent.draw()
                




    

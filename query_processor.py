import sys
import nltk
from nltk import word_tokenize, sent_tokenize ,pos_tag ,ne_chunk
from nltk.corpus import stopwords
from io_utils import read_input, output_data
from consts import intent

def process(ques):
    words = word_tokenize(ques)
    tagged = pos_tag(words)
    #namedent = ne_chunk(tagged)   #does the NER 
    #return namedent.pos()
    return tagged

question = read_input()
pos_tags = process(question)
output_data(pos_tags)
output_data(intent[pos_tags[0][1]][pos_tags[0][0]])

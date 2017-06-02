import sys
import nltk
from nltk import word_tokenize, sent_tokenize ,pos_tag ,ne_chunk
from nltk.corpus import stopwords

ques=sys.stdin.readline()

words= word_tokenize(ques)
tagged=pos_tag(words)
#namedent=ne_chunk(tagged)

#processing intent

print tagged

intent={'WRB':{'How':'Process', 'Where':'Place', 'Why':'Reason','When':'Time'},
         'WP':{'What':'Information','Who':'Person', 'Whom':'Person'},
         'WDT':{'What':'Information','Which':'Information'}
         }

#print intent['WRB']['How']

#namedent.draw()

#tag_list=[]
#tag_list=namedent.pos()
#print tag_list
#print tag_list[0]

print intent[tagged[0][1]][tagged[0][0]]


                




    

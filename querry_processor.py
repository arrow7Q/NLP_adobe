import sys
import nltk
from nltk import word_tokenize, sent_tokenize ,pos_tag ,ne_chunk
from nltk.corpus import stopwords

ques=sys.stdin.readline()

words= word_tokenize(ques)
tagged=pos_tag(words)
namedent=ne_chunk(tagged)

print tagged


intent={'WRB':{'how':'Process', 'where':'Place', 'why':'Reason','when':'Time'},
         'WP':{'what':'Information','who':'Person', 'whom':'Person'},
         'WDT':{'what':'Information','which':'Information'}
         }

#processing intent

def mode():
  for items in tagged:
      if any ( [ items[1] == 'WRB', items[1] == 'WP', items[1] == 'WDT'] ):
          return intent[items[1]][items[0]]
inten = mode()
print inten


        
#namedent.draw()

#tag_list=[]
tag_list=namedent.pos()
#print tag_list
#print tag_list[0]

#print intent[tagged[0][1]][tagged[0][0].lower()]



#doing chunking and noun phrase extraction
grammar = "NP: {<JJ>*<NN>}"

cp = nltk.RegexpParser(grammar)

result=cp.parse(tagged)
#print result 





    

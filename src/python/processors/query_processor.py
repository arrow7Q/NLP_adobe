import sys
import spacy
from spacy.en import English
from io_utils import read_input, output_data
from consts import intent , OBJECTS , VERBS, stopwords
from subverb import findSVAOs
import string

nlp = spacy.load('en')

def process(ques):
    tagged = []
    parsed = nlp(ques)
    for word in parsed:
        tupes = []
        tupes.append(word.text)
        tupes.append(word.tag_)
        tagged.append(tupes)
    return tagged

def intention(ques):
    parsed = nlp(ques)
    for items in parsed:
       if any ( [ items.tag_ == 'WRB', items.tag_ == 'WP', items.tag_ == 'WDT'] ):
           return intent[items.tag_][items.text.encode('ascii','ignore').lower()]

def types(ques):
    parsed = nlp(ques)
    que = "s"
    for item in parsed:
        if ( item.tag_ == 'WRB' and item.text.lower() == 'how' ):
            que = "STP"
        # if ( item.tag_ == 'WRB' and item.text.lower() == 'where' ):
        #     que = "PLA"
        # if ( item.tag_ == 'WP' and item.text.lower() == 'who' ):
        #     que = "PER"
        if ( item.tag_ == 'WP' and item.text.lower() == 'what' and item.head.orth_.encode('ascii') == 'is'):
            que = 'DEF' 

    if(parsed[0].tag_ in VERBS ):
        que = 'STP'

    if(que == 's'):
        que = 'DES'

    #if(parsed[0].text.lower() == "what" ):
        #que = "DE"
    return que

def nounword(ques):
    featlist = []
    
    parsed = nlp(ques)
    #for np in parsed :
    for np in parsed.noun_chunks :
        if  ( np.root.tag_ != "WP" ):
            temp = np.lemma_
            sublis = temp.split(' ')
            for i in sublis:
                
                if(i not in stopwords and i != '-PRON-'):
                    featlist.append(i)
      

        #if (np.pos_ == 'NOUN' or np.pos_ == 'PROPN'):
            #if(np.tag_ != 'WP'):
                #featlist.append(np.text)

    return featlist

def verboj(ques):
    #obj = []
    ispassive = 0
    feat= []
    parsed = nlp(ques)

    for word in parsed:
        if(word.tag_ in VERBS and word.text not in stopwords):
             feat.append(word.lemma_)

    for i in parsed.noun_chunks:
        if(i.root.dep_ == 'nsubjpass' or i.root.dep_ == 'pobj'):
            ispassive = 1
            temp = i.lemma_
            objlis = temp.split(' ')
            for i in objlis:                 
                if(i not in stopwords and i != '-PRON-'):
                    feat.append(i)



    if(ispassive != 1):
        for np in parsed.noun_chunks:
            if(np.root.dep_ in OBJECTS):
                temp = np.lemma_
                objlis = temp.split(' ')
                for i in objlis:
                    
                    if(i not in stopwords and i != '-PRON-'):
                        feat.append(i)

    #feat = pverb + ' ' + ' '.join(obj)
    return feat
    
def findsvo(ques):
    parsed = nlp(ques)
    a = findSVAOs(parsed)
    return a



exclude = set(string.punctuation)
question = read_input()
question = ''.join(ch for ch in question if ch not in exclude)
question = question.decode('utf-8').strip()
#print question
svos = findsvo(question)
pos_tags = process(question)
qtype = types(question)
if(qtype == 'STP'):
    features = verboj(question)
else:
    features = nounword(question)

res = {"pos_tags": pos_tags, "qtype": qtype, "features":features}

if __name__ == '__main__':
    #question = read_input()
    output_data(res)

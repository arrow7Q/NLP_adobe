import string
import json
import os
from lxml import etree
import nltk
from nltk import word_tokenize, sent_tokenize ,pos_tag ,ne_chunk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

path='/Users/utkarsh/codes/Help-bot/samples'


docmap=[]


for filename in os.listdir(path):
    if not filename.endswith('.xml'):continue
    fullname = os.path.join(path,filename)
    tree = etree.parse(fullname)
    root = tree.getroot()
    
    for child in root:
            newElement={}
            newElement['filename']=filename
            newElement['type']=child.tag
            newElement['text']=''.join(child.itertext()).replace('\n',' ')
            docmap.append(newElement)
        
#print json.dumps(docmap,indent=2)
#for elem in docmap:
    #print elem



from nltk.corpus import stopwords
stop=set(stopwords.words("english"))

exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

grammar= r"""
      NP:{<NN.*>}
      """

grammar2= r"""
      SVP:{<NN.*>*<VB.*>}
     
      """

cp=nltk.RegexpParser(grammar2)


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    #normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return punc_free

features=[]
for elem in docmap:
    if('body' in elem['type']):
        value=elem['text']
        #value=clean(value)
        #value=''.join(value.split())
        tokenized=word_tokenize(value)
        tagged=pos_tag(tokenized)
        #print value , '\n'
        #print tagged , '\n'
        
        result=cp.parse(tagged)
        docnoun=[]
        for subtree in result.subtrees():
            if ( subtree.label() == 'SVP' ):
                docnoun.append(subtree.leaves()[0])

        features.append(docnoun)
                
        
        
for feature in features:
    print feature
    




    

               
    



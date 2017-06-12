import json
import os
from lxml import etree
import nltk
from nltk import word_tokenize, sent_tokenize ,pos_tag ,ne_chunk
from nltk.corpus import stopwords

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
            newElement['text']=''.join(child.itertext()).replace('\n','')
            docmap.append(newElement)
        
#print json.dumps(docmap,indent=2)
#for elem in docmap:
    #print elem



from nltk.corpus import stopwords
stop_words=set(stopwords.words("english"))


for elem in docmap:
    if('body' in elem['type']):
        value=elem['text']
        #value=''.join(value.split())
        tokenized=word_tokenize(value.strip())
        filtered_value=[w for w in tokenized if not w in stop_words]
        tagged=pos_tag(tokenized)
        print filtered_value
        

    




    

               
    



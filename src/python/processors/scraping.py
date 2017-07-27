import nltk
from nltk import Tree,word_tokenize,pos_tag
import json
import os
from lxml import etree
import spacy
from spacy.en import English
from io_utils import output_data
from file_utils import absolute_path
from consts import SUBJECTS,OBJECTS,stopwords
from subverb import findSVAOs
from stepsProcessor import StepsProcessor
from xml_utils import textify


nlp = spacy.load('en')
parser = English()


path = absolute_path('../../../samples')

def lemmatize(sentence):
    sent= []
    sentence = sentence.decode('utf-8','ignore')
    parsed = nlp(sentence)
    for w in parsed:
        if(w.text not in stopwords):
            sent.append(w.lemma_)
    return ' '.join(sent)



def xapthget(tree,node):
    return tree.getpath(node)

def scrape():
    docmap=[]

    for filename in os.listdir(path):

        if filename.endswith('.ditamap') or filename.endswith('.dita') or filename.endswith('.xml'):
            fullname = os.path.join(path,filename)
            tree = etree.parse(fullname)
            root = tree.getroot()

            for child in root:
                if(child.tag == 'title' or child.tag == 'glossterm'):
                    var = ' '.join(textify(child)).replace('\n','')
                    titel =  lemmatize(var)
                if(child.tag != 'title' and child.tag != 'prolog'):
                        content = ' '.join(textify(child)).replace('\n',' ').strip()
                        if(len(content) == 0):
                            continue

                        content = content.encode('ascii','ignore')

                        pathx = xapthget(tree,child)

                        newElement={}
                        #newElement["filename"] = filename
                        newElement['title']=titel
                        if (child.tag == 'taskbody'):
                            stepsProcessor = StepsProcessor(child)
                            newElement["text"]=stepsProcessor.getStepsHTML().encode("ascii","ignore")
                            #print newElement["text"]
                        else:
                            newElement["text"]=content

                        newElement["para"] = 'true'
                        newElement['xpath'] = pathx
                        newElement['SVO'] = ''

                        docmap.append(newElement)




    return(docmap)

def linescrape(docmap):
    #docmap = []
    for filename in os.listdir(path):
        if filename.endswith('.ditamap') or filename.endswith('.dita') or filename.endswith('.xml'):
            fullname = os.path.join(path,filename)
            tree = etree.parse(fullname)
            root = tree.getroot()

            for child in root:
                if(child.tag == 'title' or child.tag == 'glossterm'):
                    var = ' '.join(textify(child)).replace('\n','')
                    titel =  lemmatize(var)

                if(child.tag != 'taskbody' and child.tag != 'title' and child.tag != 'prolog'):
                    for tag in child:
                        if(tag == 'title' or tag == 'glossterm'):
                            titel = ' '.join(textify(tag)).replace('\n',' ').strip()
                            continue

                        content = ' '.join(textify(tag)).replace('\n',' ').strip()
                        if(len(content) == 0):
                            continue
                        content = content.encode('ascii','ignore')

                        pathx = xapthget(tree,tag)


                        # newElement={}
                        # newElement["filename"] = filename
                        # newElement['title']=titel
                        # newElement["text"]=content
                        # newElement["para"] = 'false'
                        # newElement['xpath'] = pathx

                        # docmap.append(newElement)

                        content = content.decode('utf-8','ignore')
                        doc = nlp(content)
                        senlist = doc.sents
                       
                        for sent in senlist:
                            a = []
                            newElement={}
                            newElement["filename"] = filename
                            newElement['title'] = titel
                            newElement["text"] = sent.text
                            newElement["para"] = 'False'
                            newElement['xpath'] = pathx
                            svotrips = findSVAOs(sent)
                             
                            for elem in svotrips:
                                strns = ' '.join(elem)
                                a.append(strns)

                            newElement['SVO'] = a

                            docmap.append(newElement)

    #return(docmap)
    #output_data(docmap)


def parse(doc):
    grammar= r"""

        STP:{<VB.*><PRP.*>}
        STP:{<VB.*><DT>?<NN>}
        STP:{<VB.*><DT>?<JJ.*>*<NN.*>} 
        """
#DEF:{<NN.*><VB.*><NN.*>}

    cp=nltk.RegexpParser(grammar)

    for elem in doc:
        value=elem['text'].encode('ascii','ignore')
        parse = nlp(value.decode('utf-8','ignore'))
        tagged =[]
        for word in parse:
            tupe= (word.text.encode('ascii','ignore'),word.tag_.encode('ascii','ignore'))
            tagged.append(tupe)
        result = cp.parse(tagged)

        for subtree in result.subtrees():
            if ( subtree.label() == 'STP'):
                        elem['type']='STP'


            else:
                        elem['type']='DES'


    #output_data(doc)




    #output_data (doc)

def subobjadder (doc):

    for elem in doc:
        #if(elem["para"] == 'False'):
            sub =[]
            obj =[]

            words = elem['text']
            words = words.decode('utf-8','ignore')
            parsed = nlp(words)



    #adding lemmatised sub-objs
            for word in parsed.noun_chunks:
                temp1= []
                temp2 = []
                if (word.root.dep_ in SUBJECTS):

                    temp = word.lemma_
                    sublis = temp.split(' ')
                    for i in sublis:
                        
                        if(i not in stopwords and i != '-PRON-'):
                            temp1.append(i)

                    sub.append(' '.join(temp1))

                if(word.root.dep_ in OBJECTS ):
                    hold = word.lemma_
                    objlis = hold.split(' ')
                    for i in objlis:
                        
                        if(i not in stopwords  and i != '-PRON-' ):
                            temp2.append(i)
                    obj.append(' '.join(temp2))
                        

            elem['subject'] = sub
            elem['object'] =  obj

    #output_data(doc)


def tok_format(tok):
    return " -".join([tok.orth_, tok.dep_])


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)


def treevisual (doc):
    for elem in doc:
        if(elem["para"] == 'False'):
            words = elem['text']
            words = words.decode('utf-8','ignore')
            parsed = nlp(words)
            elem['tree'] = [to_nltk_tree(sent.root) for sent in parsed.sents]

    #output_data(doc)


def typedef (doc):

    for elem in doc:
        #if(elem["para"] == 'False'):
            word = elem['text']
            word = word.decode('utf-8','ignore')
            parsed = nlp(word)
            for word in parsed:
              if(word.dep_ == 'ROOT'):
                for i in word.rights:
                    if(i.dep_ == 'attr'):
                        for j in word.lefts:
                            if(j.dep_ == 'nsubj'):
                               elem['type'] = 'DEF'
                               elem['object'] = j.text


    #output_data(doc)


def addentity(doc):
    #adding entities with name
    
    for elem in doc:
        entities = []
        if( elem['para'] != 'true'):
            word = elem['text']
            word = word.decode('utf-8','ignore')
            parsed = nlp(word)
            for ent in parsed.ents:
                entity = ent.text + ' - ' + ent.label_
                entities.append(entity)

        #elem['entities'] = entities
    #outout_data(doc)



docu=scrape()
linescrape(docu)
#linescrape(docu)
parse(docu)

subobjadder(docu)
#treevisual(docu)

typedef(docu)
#addentity(docu)

if __name__ == '__main__':
    output_data(docu)
#clearparse(doc)

import sys, json

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import string
from stop_words import get_stop_words
from read_data import read_sentence

from nltk.stem import PorterStemmer, WordNetLemmatizer

lemmatiser = WordNetLemmatizer()


def filter_sentence(sentence):
  #get our data as an array from read_in()

  #print  input_sentence
  #example_sentence="In the above code we first assign S the string Hello and then in the next line we set it to the concatenated output o     !!!!"

  #example_sentence = input_sentence.translate(None, string.punctuation) #for removing punctuation

  stop_words= set(stopwords.words("english"))

  words=word_tokenize(sentence) #tokenizing

  filtered_sentence= []
  stop_words2 = get_stop_words('en')
  stop_words2 = get_stop_words('english')

  for w in words:
    if w.lower() not in stop_words:   #removing stop words list 1
      if w.lower() not in stop_words2:  #removing stop words list 2
        filtered_sentence.append(w.lower())

  lemmatized_sentence = []

  for word in filtered_sentence:
    lemmatized_sentence.append(lemmatiser.lemmatize(word))

  return " ".join(lemmatized_sentence)

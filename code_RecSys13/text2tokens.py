import random 
import math
import numpy as np
from collections import Counter
from operator import itemgetter

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

f6 = open('../review_5k_text', 'r').read()
review5k_text = eval(f6)

tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
p_stemmer = PorterStemmer()

def prep(doc):
    raw = doc.lower().replace("\n", "").replace("\t", "")
    tokens = tokenizer.tokenize(raw)
    stopped_tokens = [i for i in tokens if not i in en_stop]
    texts = [p_stemmer.stem(i) for i in stopped_tokens]
    return (" ").join(texts)
    #return texts


reviews = []
for r in xrange(len(review5k_text)):
    reviews.append(prep(review5k_text[r]))

print reviews
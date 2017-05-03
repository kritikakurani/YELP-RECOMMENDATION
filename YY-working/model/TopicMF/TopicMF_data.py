
#f1 = open('user_5k_avg', 'r').read()
#user_avg = eval(f1)

#f2 = open('business_5k_avg', 'r').read()
#business_avg = eval(f2)

f3 = open('review_5k_user', 'r').read()
review_user = eval(f3)

f4 = open('review_5k_business', 'r').read()
review_business = eval(f4)

f5 = open('review_5k_rating', 'r').read()
review_rating = eval(f5)

f6 = open('review_5k_text', 'r').read()
review_text = eval(f6)

# len(user_avg) = 4929
# len(business_avg) = 2686
# len(review_rating) = 49486
# mu = 3.7380269167037143

time = "0000"

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
p_stemmer = PorterStemmer()

def prep(doc):
    raw = doc.lower().replace("\n", "").replace("\t", "")
    tokens = tokenizer.tokenize(raw)
    # stopped_tokens = [i for i in tokens if not i in en_stop]
    # texts = [p_stemmer.stem(i) for i in stopped_tokens]
    #return (" ").join(texts)
    return tokens

for r in xrange(len(review_rating)):
    tokens = prep(review_text[r])
    print review_user[r], review_business[r], review_rating[r], time, len(tokens), (" ").join(tokens)
import random 
import math
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import NMF
from sklearn.utils.extmath import randomized_svd
from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds
from sklearn.metrics import mean_squared_error

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

f1 = open('../5k-data/user_5k_avg', 'r').read()
user_avg = eval(f1)

f2 = open('../5k-data/business_5k_avg', 'r').read()
business_avg = eval(f2)

f3 = open('../5k-data/review_5k_user', 'r').read()
review5k_user = eval(f3)

f4 = open('../5k-data/review_5k_business', 'r').read()
review5k_business = eval(f4)

f5 = open('../5k-data/review_5k_rating', 'r').read()
review5k_rating = eval(f5)

f6 = open('../5k-data/review_5k_text', 'r').read()
review5k_text = eval(f6)

#f7 = open('relation_5k', 'r').read()
#relation = eval(f7)

random_test = random.sample(xrange(len(review5k_rating)), 1000)

train_user = []
train_business = []
train_rating = []
train_text = []

test_user = []
test_business = []
test_rating = []

for r in xrange(len(review5k_rating)):
    if r in random_test:
        test_user.append(review5k_user[r])
        test_business.append(review5k_business[r])
        test_rating.append(review5k_rating[r])
    else:
        train_user.append(review5k_user[r])
        train_business.append(review5k_business[r])
        train_rating.append(review5k_rating[r])
        train_text.append(review5k_text[r])
        
K_topic = 10
Times = 50
DocWord = 300
DocTopic = 5

sim_val = 0.85 # default = 0.85
vip_val = 0.20 # default = 0.20

num_user = len(user_avg)
num_business = len(business_avg)
num_train = len(train_rating)
num_test = len(test_rating)

mu = np.mean(train_rating)

tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
p_stemmer = PorterStemmer()

def prep(doc):
    raw = doc.lower().replace("\n", "").replace("\t", "")
    tokens = tokenizer.tokenize(raw)
    stopped_tokens = [i for i in tokens if not i in en_stop]
    texts = [p_stemmer.stem(i) for i in stopped_tokens]
    return (" ").join(texts)

from sklearn import linear_model
def MLR(X, Y):
    reg = linear_model.LinearRegression()
    reg.fit(X, Y)
    return reg.coef_

Ubb = []
for i in xrange(num_user):
    Ubb.append([])
    for j in xrange(num_business):
        val = user_avg[i] + business_avg[j] - mu
        if val < 1: val = 1
        if val > 5: val = 5
        Ubb[i].append(val) 

Breview = [""]*num_business
for r in xrange(num_train):
    Breview[train_business[r]] += prep(train_text[r])

tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=DocWord, stop_words='english')
tf = tf_vectorizer.fit_transform(Breview)

lda = LatentDirichletAllocation(n_topics=DocTopic, max_iter=5, learning_method='online',learning_offset=50.,random_state=0)
DocTopDist = lda.fit_transform(tf)

row = np.array([])
col = np.array([])
val = np.array([])

# delta -> difference between rating and ubb [u*b], delta2 -> rating boolean
delta = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
delta2 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
for r in xrange(num_train):
    delta[train_user[r]][train_business[r]] = train_rating[r] - Ubb[train_user[r]][train_business[r]]
    delta2[train_user[r]][train_business[r]] = 1

deltaReg = []
for i in xrange(num_user):
    X = [[0,0,0,0,0], [1,0,0,0,0], [0,1,0,0,0], [0,0,1,0,0], [0,0,0,1,0], [0,0,0,0,1]]; Y = [0,0,0,0,0,0]
    for j in xrange(num_business):
        if delta2[i][j]:
            X.append(list(DocTopDist[j]))
            Y.append(delta[i][j])
    coef = MLR(X, Y)
    deltaReg.append(np.dot(DocTopDist, coef))
    
row = np.array([])
col = np.array([])
val = np.array([])
TopicIn = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
for i in xrange(num_user):
    for j in xrange(num_business):
        val = Ubb[i][j] + math.atan(deltaReg[i][j])
        if val < 1: val = 1
        if val > 5: val = 5
        TopicIn[i][j] = val

TopicInPd = []
for r in xrange(num_test):
    TopicInPd.append(TopicIn[test_user[r]][test_business[r]]) 

TopicInPd_rmse = mean_squared_error(test_rating, TopicInPd)  
print TopicInPd_rmse


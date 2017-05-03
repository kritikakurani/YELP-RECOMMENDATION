import random 
import math
import numpy as np
from operator import itemgetter
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


f = open('../new_5k/5k-data', 'r')
business_name = eval(f.readline())
business_avg = eval(f.readline())
user_name = eval(f.readline())
user_avg = eval(f.readline())

f = open('../new_5k/5k-relation', 'r').read()
relation = eval(f)

f = open('../new_5k/5k-review', 'r')
review5k_business = eval(f.readline())
review5k_user = eval(f.readline())
review5k_rating = eval(f.readline())
review5k_text = eval(f.readline())

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

#lbd0 = 0.35 # Topic effect
#lbd1 = 0.35 # Similarity effect 
#lbd2 = 0.35 # relation afftect
#lbd3 = 0.35 # VIP effect
lbd4 = 0.35 # Topic effect in Tri-model
lbd5 = 0.35 # VIP effect in Tri-model

num_user = len(user_avg)
num_business = len(business_avg)
num_train = len(train_rating)
num_test = len(test_rating)

mu = np.mean(train_rating)

def float2int(f):
    if f < 1.5: return 1
    if f < 2.5: return 2
    if f < 3.5: return 3
    if f < 4.5: return 4
    return 5

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

Rij = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
Sij = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
Tij = csr_matrix((val,(row,col)), shape=(num_user,num_user)).toarray()
Uij = csr_matrix((val,(row,col)), shape=(num_user,num_user)).toarray()
Vij = csr_matrix((val,(row,col)), shape=(num_user,num_user)).toarray()

# user-item rating matrix. If ui gives a rating to vj, Rij is the rating score, otherwise 0
for r in xrange(num_train):
    Rij[train_user[r]][train_business[r]] = train_rating[r] - Ubb[train_user[r]][train_business[r]]
    Sij[train_user[r]][train_business[r]] = 1
       
# user-user social relations where Tij = 1 if ui,uj has a relation and zero otherwise
for u in relation:
    for f in u[1]:
        Tij[u[0]][f] = 1

# VIP matrix where Uij = 1 if uj is a VIP and zero otherwise        
PR = {}
for u in relation:
    PR[u[0]] = len(u[1])    
sorted_PR = sorted(PR.items(), key=itemgetter(1), reverse=True)
rank = {}
for u in xrange(num_user):
    rank[sorted_PR[u][0]] = u+1
Wi = []
for u in xrange(num_user):
    Wi.append(1.0/(1.0+ math.log(rank[u])))

for u in xrange(num_user):
    for v in xrange(num_user):
        Uij[u][v] = Wi[v]
        Vij[u][v] = 1

# user-user similarity
Cos_norm = []
for u in xrange(num_user):
    Cos_norm.append(math.sqrt(np.dot(Rij[u], Rij[u])))

Cos = np.dot(Rij, Rij.T)
for i in xrange(num_user):
    for j in xrange(num_user):
        if Cos_norm[i] and Cos_norm[j]:
            Cos[i][j] = Cos[i][j]/Cos_norm[i]/Cos_norm[j]
        else: 
            Cos[i][j] = 0

TR = np.dot(Tij, Rij)
TS = np.dot(Tij, Sij)
UR = np.dot(Uij, Rij)
VS = np.dot(Uij, Sij)
CR = np.dot(Cos, Rij)

row = np.array([])
col = np.array([])
val = np.array([])
Vij1 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
Vij2 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
Vij3 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()


for i in xrange(num_user):
    for j in xrange(num_business):
        if TS[i][j]: Vij1[i][j] = TR[i][j]/TS[i][j]
        if VS[i][j]: Vij2[i][j] = UR[i][j]/VS[i][j]
        if num_user: Vij3[i][j] = CR[i][j]/num_user 

row = np.array([])
col = np.array([])
val = np.array([])
Tri = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()

for i in xrange(num_user):
    for j in xrange(num_business):
        val = Ubb[i][j] + lbd4*deltaReg[i][j] + lbd5*Vij2[i][j]
        
        if val1 < 1: val1 = 1
        if val1 > 5: val1 = 5
        if val2 < 1: val2 = 1
        if val2 > 5: val2 = 5
        if val3 < 1: val3 = 1
        if val3 > 5: val3 = 5
            
        Tri[i][j] = val

TriPd = []
for r in xrange(num_test):
    TriPd.append(Tri[test_user[r]][test_business[r]]) 

TriPd_rmse = mean_squared_error(test_rating, TriPd)  
print TriPd_rmse
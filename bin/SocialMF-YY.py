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

f7 = open('../5k-data/relation_5k', 'r').read()
relation = eval(f7)

random_test = random.sample(xrange(len(review5k_rating)), 1000)

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
vip_val = 0.2
lbd1 = 0.5 # Similarity effect 
lbd2 = 0.5 # relation afftect
lbd3 = 0.5 # VIP effect

num_user = len(user_avg)
num_business = len(business_avg)
num_train = len(train_rating)
num_test = len(test_rating)

mu = np.mean(train_rating)

Ubb = []
for i in xrange(num_user):
    Ubb.append([])
    for j in xrange(num_business):
        val = user_avg[i] + business_avg[j] - mu
        if val < 1: val = 1
        if val > 5: val = 5
        Ubb[i].append(val) 

PR = {}
for u in relation:
    PR[u[0]] = len(u[1])
    
from operator import itemgetter
sorted_PR = sorted(PR.items(), key=itemgetter(1), reverse=True)

rank = {}
for u in xrange(num_user):
    rank[sorted_PR[u][0]] = u+1

Ri = []
for u in xrange(num_user):
    Ri.append(rank[u])

Wi = []
for ri in Ri:
    Wi.append(1.0/(1.0+ math.log(ri)))    

row = np.array([])
col = np.array([])
val = np.array([])

Rij = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
Sij = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
Tij = csr_matrix((val,(row,col)), shape=(num_user,num_user)).toarray()
Uij = csr_matrix((val,(row,col)), shape=(num_user,num_user)).toarray()

# user-item rating matrix. If ui gives a rating to vj, Rij is the rating score, otherwise 0
for r in xrange(num_train):
    Rij[train_user[r]][train_business[r]] = train_rating[r] - Ubb[train_user[r]][train_business[r]]
    Sij[train_user[r]][train_business[r]] = 1
       
# user-user social relations where Tij = 1 if ui,uj has a relation and zero otherwise
for u in relation:
    for f in u[1]:
        Tij[u[0]][f] = 1

# VIP matrix where Uij = 1 if uj is a VIP and zero otherwise        
for u in xrange(num_user):
    for v in xrange(num_user):
        if Wi[v] > vip_val:
            Uij[u][v] = 1

TR = np.dot(Tij, Rij)
TS = np.dot(Tij, Sij)
UR = np.dot(Uij, Rij)
US = np.dot(Uij, Sij)

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

CR = np.dot(Cos, Rij)
CS = np.dot(Cos, Sij)

row = np.array([])
col = np.array([])
val = np.array([])
Vij1 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
Vij2 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
Vij3 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()


for i in xrange(num_user):
    for j in xrange(num_business):
        if US[i][j]: Vij3[i][j] = lbd3*UR[i][j]/US[i][j]
        if TS[i][j]: Vij2[i][j] = lbd2*TR[i][j]/TS[i][j]
        if CS[i][j]: Vij1[i][j] = lbd1*CR[i][j]/CS[i][j]   

row = np.array([])
col = np.array([])
val = np.array([])
SocialIn = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()

for i in xrange(num_user):
    for j in xrange(num_business):
        val = Ubb[i][j] + (Vij1[i][j] + Vij2[i][j] + Vij3[i][j])/3
        
        if val < 1: val = 1
        if val > 5: val = 5
        SocialIn[i][j] = val1


SocialInPd = []
for r in xrange(num_test):
    SocialInPd.append(SocialIn[test_user[r]][test_business[r]]) 

SocialInPd_rmse = mean_squared_error(test_rating, SocialInPd1)   

print SocialInPd_rmse


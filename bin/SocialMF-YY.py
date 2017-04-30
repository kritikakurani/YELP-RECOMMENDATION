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

    Breview[train_business[r]] += prep(train_text[r])

row = np.array([])
col = np.array([])
val = np.array([])
Vij1 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
Vij2 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
Vij3 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()


for i in xrange(num_user):
    for j in xrange(num_business):
        if TS[i][j]: Vij1[i][j] = lbd1*TR[i][j]/TS[i][j]
        if VS[i][j]: Vij2[i][j] = lbd2*UR[i][j]/VS[i][j]
        if num_user: Vij3[i][j] = lbd3*CR[i][j]/num_user 

row = np.array([])
col = np.array([])
val = np.array([])
SocialIn1 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
SocialIn2 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
SocialIn3 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()

for i in xrange(num_user):
    for j in xrange(num_business):
        val1 = Ubb[i][j] + Vij1[i][j]
        val2 = Ubb[i][j] + Vij2[i][j]
        val3 = Ubb[i][j] + Vij3[i][j]
        
        if val1 < 1: val1 = 1
        if val1 > 5: val1 = 5
        if val2 < 1: val2 = 1
        if val2 > 5: val2 = 5
        if val3 < 1: val3 = 1
        if val3 > 5: val3 = 5
            
        SocialIn1[i][j] = val1
        SocialIn2[i][j] = val2
        SocialIn3[i][j] = val3

SocialInPd1 = []
SocialInPd2 = []
SocialInPd3 = []
for r in xrange(num_test):
    SocialInPd1.append(SocialIn1[test_user[r]][test_business[r]]) 
    SocialInPd2.append(SocialIn2[test_user[r]][test_business[r]]) 
    SocialInPd3.append(SocialIn3[test_user[r]][test_business[r]]) 

SocialInPd_rmse1 = mean_squared_error(test_rating, SocialInPd1)  
SocialInPd_rmse2 = mean_squared_error(test_rating, SocialInPd2)  
SocialInPd_rmse3 = mean_squared_error(test_rating, SocialInPd3)  

print "relation rmse =", SocialInPd_rmse1
print "VIP rmse =", SocialInPd_rmse2
print "similarity rmse =", SocialInPd_rmse3

if SocialInPd_rmse1 < SocialInPd_rmse2 and SocialInPd_rmse1 < SocialInPd_rmse3:
    print "relation between users dominant rating"
    SocialInPd_rmse = SocialInPd_rmse1
elif SocialInPd_rmse2 < SocialInPd_rmse3:
    print "VIP user dominant rating"
    SocialInPd_rmse = SocialInPd_rmse2
else:
    print "user similarity dominant rating"
    SocialInPd_rmse = SocialInPd_rmse3

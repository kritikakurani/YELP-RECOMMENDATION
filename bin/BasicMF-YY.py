import random 
import math
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import NMF
from sklearn.utils.extmath import randomized_svd
from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds
from sklearn.metrics import mean_squared_error

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

#f6 = open('review_5k_text', 'r').read()
#review5k_text = eval(f6)

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
        #train_text.append(review5k_text[r])
        
K_topic = 10
Times = 50

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

UbbPd = []
for r in xrange(num_test):
    UbbPd.append(Ubb[test_user[r]][test_business[r]]) 

#UbbPdInt = []
#for r in UbbPd: 
#    UbbPdInt.append(float2int(r)) 

Ubb_rmse = mean_squared_error(test_rating, UbbPd)  
#UbbPdInt_rmse = mean_squared_error(test_rating, UbbPdInt) 

print Ubb_rmse
#print UbbPdInt_rmse

BasicIn = []
for i in xrange(num_user):
    BasicIn.append([])
    for j in xrange(num_business):
        val = user_avg[i] + business_avg[j] - mu
        if val < 1: val = 1
        if val > 5: val = 5
        BasicIn[i].append(val) 
        
for r in xrange(num_train):
    BasicIn[train_user[r]][train_business[r]] = train_rating[r]

model = NMF(n_components=K_topic, init='random', random_state=0)
U = model.fit_transform(BasicIn);
V = model.components_;
BasicOut = np.dot(U,V)

BasicPd = []
for r in xrange(num_test):
    BasicPd.append(BasicOut[test_user[r]][test_business[r]]) 

#BasicPdInt = []
#for r in BasicPd: 
#    BasicPdInt.append(float2int(r)) 

BasicPd_rmse = mean_squared_error(test_rating, BasicPd)  
#BasicPdInt_rmse = mean_squared_error(test_rating, BasicPdInt) 

print BasicPd_rmse
#print BasicPdInt_rmse

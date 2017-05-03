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

file = open('result.res','a')
f = open('new_5k/5k-data', 'r')
business_name = eval(f.readline())
business_avg = eval(f.readline())
user_name = eval(f.readline())
user_avg = eval(f.readline())

f = open('new_5k/5k-relation', 'r').read()
relation = eval(f)

f = open('new_5k/5k-review', 'r')
review5k_business = eval(f.readline())
review5k_user = eval(f.readline())
review5k_rating = eval(f.readline())
review5k_text = eval(f.readline())

fold_size = len(review5k_rating) / 10

total_relation_rmse = []
for n in xrange(10):
    total_relation_rmse.append(0)
total_VIP_rmse = []
for n in xrange(10):
    total_VIP_rmse.append(0)
total_similarity_rmse = []
for n in xrange(10):
    total_similarity_rmse.append(0)
    

for fold in range(10):
    print "%s fold: " % (fold)
    file.writelines("%s fold: \n" % (fold))
    random_test = random.sample(xrange(len(review5k_rating)), 1000)

    train_user = []
    train_business = []
    train_rating = []
    train_text = []

    test_user = []
    test_business = []
    test_rating = []

    for r in xrange(len(review5k_rating)):
        if ( fold * fold_size < r and r < (fold+1) * fold_size  ):
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
            Uij[u][v] = Wi[v]

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
    US = np.dot(Uij, Sij)
    CR = np.dot(Cos, Rij)
    CS = np.dot(Cos, Sij)

    row = np.array([])
    col = np.array([])
    val = np.array([])
    Vij1 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
    Vij2 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
    Vij3 = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()

    for n in xrange(10):
        lbd = 0.1*(n+1)
        print "social model lbd=",lbd
        file.writelines("social model lbd= %f\n" % (lbd))
        for i in xrange(num_user):
            for j in xrange(num_business):
                if TS[i][j]: Vij1[i][j] = lbd*TR[i][j]/TS[i][j]
                if US[i][j]: Vij2[i][j] = lbd*UR[i][j]/US[i][j]
                if CS[i][j]: Vij3[i][j] = lbd*CR[i][j]/CS[i][j]

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

        # print 'relation,',SocialInPd_rmse1
        file.writelines('relation:%f\n' % (SocialInPd_rmse1))
        total_relation_rmse[n] += SocialInPd_rmse1
        # print 'VIP,',SocialInPd_rmse2
        file.writelines('VIP:%f\n' % (SocialInPd_rmse2))
        total_VIP_rmse[n] += SocialInPd_rmse2
        # print 'similarity',SocialInPd_rmse3
        file.writelines('similarity:%f\n' % (SocialInPd_rmse3))
        total_similarity_rmse[n] += SocialInPd_rmse3


for b in xrange(10):
    id = 0.1*(b+1)
    # print id,
    file.write('%f' % (id))
    # print 'total relation,',
    file.writelines('total relation:%f\n' % (total_relation_rmse[b]/10.))
    # print total_relation_rmse[b]/10.
    # print 'total VIP,',
    file.writelines('total vip:%f\n' % (total_VIP_rmse[b]/10.))
    # print total_VIP_rmse[b]/10.
    # print 'total similarity',
    file.writelines('total similarity:%f\n' % (total_similarity_rmse[b]/10.))
    # print total_similarity_rmse[b]/10.





import numpy as np
from scipy.sparse import csr_matrix
from sklearn.utils.extmath import randomized_svd
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

f1 = open('user_5k_avg', 'r').read()
user_avg = eval(f1)

f2 = open('business_5k_avg', 'r').read()
business_avg = eval(f2)

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

mu = np.mean(review_rating)

uv = []
for r in xrange(len(review_rating)):
	uv.append(review_rating[r] - user_avg[review_user[r]] - business_avg[review_business[r]] + mu) 

row = np.array(review_business)
col = np.array(review_user)
val = np.array(review_rating)
ori = csr_matrix((val,(row,col)), shape=(len(business_avg),len(user_avg))).toarray()
val = np.array(uv)
rec = csr_matrix((val,(row,col)), shape=(len(business_avg),len(user_avg))).toarray()

tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
p_stemmer = PorterStemmer()

def prep(doc):
	raw = doc.lower().replace("\n", "").replace("\t", "")
	tokens = tokenizer.tokenize(raw)
	stopped_tokens = [i for i in tokens if not i in en_stop]
	texts = [p_stemmer.stem(i) for i in stopped_tokens]
	return (" ").join(texts)

business_review = [""]*len(business_avg)
for r in xrange(len(review_business)):
	business_review[review_business[r]] += prep(review_text[r])

n_features = 300 # f
n_topics = 30

#LDA requires data in the form of integer counts. So modifying feature values using TF-IDF and then using with LDA doesn't really fit in.
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features, stop_words='english')
tf = tf_vectorizer.fit_transform(business_review)
tf_feature_names = tf_vectorizer.get_feature_names()
tf_vocabulary = tf_vectorizer.vocabulary_
# tf: matrix [2686 * f] Use tf (raw term count) features for LDA.
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5, learning_method='online',learning_offset=50.,random_state=0)
theta = lda.fit_transform(tf) # U
phi = lda.components_	# V

def matrix_factorization(R, P, Q, K, N, M, steps=5000, alpha=0.0002, beta=0.02):
    for step in xrange(steps):
        for i in xrange(N):
            for j in xrange(M):
                if R[i][j] > 0: eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        
        eR = np.dot(P,Q)
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
        if e < 0.001:
            break
        
    return P, Q

def YYMF(R, P, Q, K, N, M, steps=5000, alpha=0.0002, beta=0.02):
	for step in xrange(steps):
		print "hello"
		T = np.dot(P,Q)
		for i in xrange(N):
			for j in xrange(M):
				if R[i][j] > 0: 
					eij = R[i][j] - T[i][j]
					for k in xrange(K):
						Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
	return P, Q


R = ori
N = len(R)
M = len(R[0])
K = n_topics
P = theta
Q = np.random.rand(K,M)

nP, nQ = YYMF(R, P, Q, K, N, M)
now = np.dot(nP, nQ)
rmse = mean_squared_error(ori, now)












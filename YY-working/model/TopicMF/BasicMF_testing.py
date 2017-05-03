import numpy as np
import matplotlib.pylab as plt
from scipy.sparse import csr_matrix
from sklearn.utils.extmath import randomized_svd
from sklearn.metrics import mean_squared_error

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

#f6 = open('review_5k_text', 'r').read()
#review_text = eval(f6)

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
val = np.array(uv)
ori = csr_matrix((val,(row,col)), shape=(len(business_avg),len(user_avg))).toarray()

# n_comp = 30 # k
n_iter = 15

def BMF(n_comp, n_iter):
	U, S, VT = randomized_svd(ori, n_components=n_comp, n_iter=n_iter, random_state=None)

	rc = []
	for n in xrange(n_comp):
		rc.append(n)
	rc = np.array(rc)
	S = csr_matrix((S,(rc,rc)), shape=(n_comp, n_comp)).toarray()

	new = np.dot(np.dot(U,S),VT)

	rmse = mean_squared_error(ori, new)

	return rmse

res = {}
for n in xrange(20):
	n_comp = 5*(n+1)
	rmse = BMF(n_comp, n_iter)
	res[n_comp] = rmse

	print n_comp, "\t", rmse

lists = sorted(res.items()) 
x, y = zip(*lists) 

plt.bar(x, y, width = 4.5)
plt.xticks(np.arange(min(x), max(x)+1, 10))
#plt.xticks(np.arange(min(x), max(x)+1, 0.05))

plt.xlabel("n_comp")
plt.ylabel("rmse")
plt.title("Basic Model")
plt.savefig("BasicMF_ncomp")


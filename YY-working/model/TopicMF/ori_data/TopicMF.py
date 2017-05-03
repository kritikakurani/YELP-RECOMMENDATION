import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import NMF
from sklearn.metrics import mean_squared_error

f1 = open('user_avg.data', 'r').read()
user_avg = eval(f1)

f2 = open('business_avg.data', 'r').read()
business_avg = eval(f2)

f3 = open('review_user.data', 'r').read()
review_user = eval(f3)

f4 = open('review_business.data', 'r').read()
review_business = eval(f4)

#f5 = open('review_rating.data', 'r').read()
#review_rating = eval(f5)

f6 = open('review_text.data', 'r').read()
review_text = eval(f6)

row = np.array(review_business)
col = np.array(review_user)
val = np.array(review_rating)
rating_matrix = csr_matrix((val,(row,col)), shape=(len(business_avg),len(user_avg))).toarray()
model = NMF(n_components=30, init='random', random_state=0)
U = model.fit_transform(rating_matrix)
V = model.components_

print U.tolist()
print V.tolist()
print np.dot(U,V).tolist()
print error
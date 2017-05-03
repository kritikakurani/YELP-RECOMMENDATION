simimport math
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.utils.extmath import randomized_svd
from sklearn.metrics import mean_squared_error

f1 = open('user_5k_avg', 'r').read()
user_avg = eval(f1)

f2 = open('business_5k_avg', 'r').read()
business_avg = eval(f2)

f1 = open('review_5k_user', 'r').read()
review_5k_user = eval(f1)

f2 = open('review_5k_business', 'r').read()
review_5k_business = eval(f2)

f3 = open('review_5k_rating', 'r').read()
review_5k_rating = eval(f3)

f4 = open('relation_5k', 'r').read()
relation_5k = eval(f4)

num_user = 4929
num_business = 2686
num_review = 49486

row = np.array([])
col = np.array([])
val = np.array([])

Rij = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
for r in xrange(num_review):
    Rij[review_5k_user[r]][review_5k_business[r]] = review_5k_rating[r]

Tij = csr_matrix((val,(row,col)), shape=(num_user,num_user)).toarray()
for u in relation_5k:
    for f in u[1]:
        Tij[u[0]][f] = 1

Sij_norm = []
for u in xrange(num_user):
    Sij_norm.append(math.sqrt(np.dot(Rij[u], Rij[u])))

Sij = csr_matrix((val,(row,col)), shape=(num_user,num_user)).toarray()
for i in xrange(num_user):
    for j in xrange(num_user):
        if Sij_norm[i] and Sij_norm[j]:
            Sij[i][j] = Sij[i][j]/Sij_norm[i]/Sij_norm[j]
        else: 
            Sij[i][j] = 0

import networkx as nx
node_list = []
for u in xrange(num_user):
    node_list.append(u)
G=nx.Graph()
G.add_nodes_from(node_list)

for u in relation_5k:
    for f in u[1]:
        G.add_edge(u[0], f)
PR = nx.pagerank(G)

from operator import itemgetter
sorted_PR = sorted(PR.items(), key=itemgetter(1), reverse=True)

rank = {}
for u in xrange(num_user):
    rank[sorted_PR[u][0]] = u

Ri = []
for u in xrange(num_user):
    Ri.append(rank[u]+1)

Wi = []
for ri in Ri:
    Wi.append(1.0/(1.0+ math.log(ri)))

Wij = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
for i in xrange(num_user):
    for j in xrange(num_business):
        if Rij[i][j] > 0:
            Wij[i][j] = math.sqrt(Wi[i])



# G.number_of_nodes() = 4929
# G.number_of_edges() = 32526








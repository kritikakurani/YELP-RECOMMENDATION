#social model:
import math
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics import mean_squared_error
import networkx as nx
import matplotlib.pyplot as plt
from time import time
from operator import itemgetter
import networkx as nx

def matrix_factorization(R, P, Q, K, S, H, N, Si, steps=5000, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in xrange(steps):
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] * S[i][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] * S[i][j]- beta * Q[k][j])
            for m in N[i]:
                Eim=Si[i][m]-np.sum(P[i,:]*H*P[j,:]);
                for k in xrange(K):
                    P[i][k]=P[i][k]+alpha*(2 * Eim * beta * H[k] * P[m][k]);
                    H[k]=H[k]+ alpha*(2 * Eim * beta * P[i][k] * P[m][k]);
        eR = np.dot(P,Q)
        e = 0
        E= 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
            for m in N[i]:
                E = E + pow(Si[i][m]-np.sum(P[i,:]*H*P[j,:]),2);
        if e + E/2 < 0.001:
            break
    return P, Q.T, H
	
def performance(P, Q, R, none_zero):
    num=len(none_zero)
    Q=Q.T;
    r=np.dot(P,Q);
    error=0;
    for p in none_zero:
        i=p[0];
        j=p[1];
        error+=(R[i][j]-r[i][j])*(R[i][j]-r[i][j]);
        #print R[i][j]-r[i][j]
    error=math.sqrt(error/num);
    return error;
	
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
Nij=[[]]*num_user;

for r in relation_5k:
    Nij[r[0]]=r[1];
	
row = np.array([])
col = np.array([])
val = np.array([])

Tij = csr_matrix((val,(row,col)), shape=(num_user,num_user)).toarray()
for u in relation_5k:
    for f in u[1]:
        Tij[u[0]][f] = 1
		
none_zero=[];
Rij = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
for r in xrange(num_review):
    Rij[review_5k_user[r]][review_5k_business[r]] = review_5k_rating[r];
    none_zero.append([review_5k_user[r],review_5k_business[r]]);
	
Sij_norm = []
for u in xrange(num_user):
    Sij_norm.append(math.sqrt(np.dot(Rij[u], Rij[u])))
	
Sij = np.dot(Rij, Rij.T)

for i in xrange(num_user):
    for j in xrange(num_user):
        if Sij_norm[i] and Sij_norm[j]:
            Sij[i][j] = Sij[i][j]/Sij_norm[i]/Sij_norm[j]
        else:
            Sij[i][j]=0

node_list = []
for u in xrange(num_user):
    node_list.append(u)
	
G=nx.Graph()
G.add_nodes_from(node_list)
for u in relation_5k:
    for f in u[1]:
        G.add_edge(u[0], f)
		
PR = nx.pagerank(G)

sorted_PR = sorted(PR.items(), key=itemgetter(1), reverse=True)

rank = {}
for u in xrange(num_user):
    rank[sorted_PR[u][0]] = u
	
Ri = []
for u in xrange(num_user):
    Ri.append(rank[u]+1)
	
Wij = csr_matrix((val,(row,col)), shape=(num_user,num_business)).toarray()
for i in xrange(num_user):
    for j in xrange(num_business):
        if Rij[i][j] > 0:
            Wij[i][j] = math.sqrt(Ri[i])
			
n=10
testnum=num_review*0.1
times=100
total=len(none_zero)
k=30
rmse=0.
steps=1000
start=time();
truetimes=0.
for x in xrange(times):
    chose=np.random.randint(0,total,size=testnum)
    not_chose=list(set(range(0,total))-set(chose))
    trainmat = np.copy(Rij)
    train_none_zero=list(none_zero[i] for i in not_chose)
    for p in chose:
        i=none_zero[p][0]
        j=none_zero[p][1]
        trainmat[i][j]=0
    test_none_zero=list(none_zero[i] for i in chose)
    P = np.random.rand(num_user,k)
    Q = np.random.rand(num_business,k)
    H = np.random.rand(k)
    nP,nQ,nH= matrix_factorization(trainmat, P, Q, k, Wij, H, Nij, Sij, steps, 0.0002, 0.02)
    rmse=performance(nP,nQ,Rij,test_none_zero)+rmse;
    truetimes=1+truetimes;
    if(time()-start>36000):
        break;
    
print rmse/truetimes;

import math
import matplotlib.pylab as plt
import numpy as np

u = open('cluster_location.data', 'r').read()
cluster = eval(u)

d = {}
for c in cluster:
	d[c[0]] = (len(c[1]))

xname = "cluster"
yname = "count(business)"
title_name = "distribution of business"
fig_name = "cluster-business-stat"

lists = sorted(d.items()) 
x, y = zip(*lists) 

plt.bar(x, y, width = 0.4)
plt.xticks(np.arange(min(x), max(x)+1, 10))
plt.xticks(np.arange(min(x), max(x)+1, 10))
plt.xlabel(xname)
plt.ylabel(yname)
plt.title(title_name)
plt.savefig(fig_name)





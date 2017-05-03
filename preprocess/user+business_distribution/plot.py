import math
import matplotlib.pylab as plt
import numpy as np

u = open('user-stat.out', 'r').read()
user = eval(u)

b = open('business-stat.out', 'r').read()
business = eval(b)

review_count  = user[0]
average_stars = user[5]

reviews = business[0]
stars = business[1]

'''
review_count_log = {}
for k in review_count:
	review_count_log[int(k/30)] = 0 
for k in review_count:
	review_count_log[int(k/30)] += review_count[k]
for k in review_count_log:
	review_count_log[k] = 1.0*math.log(review_count_log[k]+1.0)
d = review_count_log
xname = "count(review)/30"
yname = "log( count(user) )"
title_name = "distribution of reviews per user"
fig_name = "userfig_review_count"
'''

review_count_log = {}
for k in reviews:
	review_count_log[int(k/30)] = 0 
for k in reviews:
	review_count_log[int(k/30)] += reviews[k]
for k in review_count_log:
	review_count_log[k] = 1.0*math.log(review_count_log[k]+1.0)
d = review_count_log
xname = "count(review)/30"
yname = "log( count(business) )"
title_name = "distribution of reviews per business"
fig_name = "businessfig_review_count"


lists = sorted(d.items()) 
x, y = zip(*lists) 

plt.plot(x, y)
#plt.xticks(np.arange(0, 100, 20))
#plt.yticks(np.arange(0, 15, 2))
plt.xlabel(xname)
plt.ylabel(yname)
plt.title(title_name)
plt.savefig(fig_name)





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

'''review_count_log = {}
for k in review_count:
	review_count_log[k/100] = 0 
for k in review_count:
	review_count_log[k/100] += review_count[k]
for k in review_count_log:
	review_count_log[k] = 1.0*math.log(review_count_log[k]+1.0)
d = review_count_log
xname = "count(review)/100"
yname = "log( count(user) )"
title_name = "distribution of reviews per user"
fig_name = "userfig_review_count"'''

'''review_count_log = {}
for k in review_count:
	review_count_log[int(math.log(k+1.0))] = 0 
for k in review_count:
	review_count_log[int(math.log(k+1.0))] += review_count[k]
for k in review_count_log:
	review_count_log[k] = 1.0*math.log(review_count_log[k]+1.0)
d = review_count_log
xname = "log( count(review) )"
yname = "log( count(user) )"
title_name = "distribution of reviews per user"
fig_name = "userfig_review_count2"'''

'''avg_stars = {}
for k in average_stars:
	avg_stars[int(k*2)/2.0] = 0
for k in average_stars:
	avg_stars[int(k*2)/2.0] += average_stars[k]
d = avg_stars
xname = "average_stars"
yname = "log( count(user))"
title_name = "distribution of average stars of user"
fig_name = "userfig_avg_stars"'''

'''review_count_log = {}
for k in reviews:
	review_count_log[k/100] = 0 
for k in reviews:
	review_count_log[k/100] += reviews[k]
for k in review_count_log:
	review_count_log[k] = 1.0*math.log(review_count_log[k]+1.0)
d = review_count_log
xname = "count(review)/100"
yname = "log( count(user) )"
title_name = "distribution of reviews per user"
fig_name = "businessfig_review_count"'''

'''review_count_log = {}
for k in reviews:
	review_count_log[int(math.log(k+1.0))] = 0 
for k in reviews:
	review_count_log[int(math.log(k+1.0))] += reviews[k]
for k in review_count_log:
	review_count_log[k] = 1.0*math.log(review_count_log[k]+1.0)
d = review_count_log
xname = "log( count(review) )"
yname = "log( count(business) )"
title_name = "distribution of reviews per business"
fig_name = "businessfig_review_count2"'''

avg_stars = {}
for k in stars:
	avg_stars[int(k*2)/2.0] = 0
for k in stars:
	avg_stars[int(k*2)/2.0] += stars[k]
d = avg_stars
xname = "average_stars"
yname = "log( count(business))"
title_name = "distribution of average stars of business"
fig_name = "businessfig_avg_stars"

lists = sorted(d.items()) 
x, y = zip(*lists) 

plt.bar(x, y, width = 0.4)
plt.xticks(np.arange(min(x), max(x)+1, 0.5))
plt.xticks(np.arange(min(x), max(x)+1, 0.5))
plt.xlabel(xname)
plt.ylabel(yname)
plt.title(title_name)
plt.savefig(fig_name)





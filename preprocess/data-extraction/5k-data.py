import os
import datetime
import json
import re
import math
import numpy as np
import operator
import collections

o = open('./subset/business_subset.data', 'r').read()
business_subset = eval(o)
business_name = []
business_avg = []
for b in business_subset:
	if b[1] > 30:
		business_name.append(b[0])
		business_avg.append(b[2])

o = open('./subset/user_subset.data', 'r').read()
user_subset = eval(o)
user_avg_dict = {}
user1 = []
for u in user_subset:
	if u[1] > 50:
		user_avg_dict[u[0]] = u[2]
		user1.append(u[0])

o = open('./subset/relation_subset.data', 'r').read()
relation_subset = eval(o)
user2 = []
for u in relation_subset:
	if len(u[1]) > 50:
		user2.append(u[0])

user_name = list(set(user1).intersection(user2))
user_avg = []
for u in user_name:
	user_avg.append(user_avg_dict[u])

print business_name
print business_avg
print user_name
print user_avg

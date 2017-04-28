import os
import datetime
import json
import re
import math
import numpy as np
import operator
import collections



f = open('./5k-data', 'r')
business_name = eval(f.readline())
business_avg = eval(f.readline())
user_name = eval(f.readline())
user_avg = eval(f.readline())

user_dict = {}
for u in xrange(len(user_name)):
	user_dict[user_name[u]] = u

o = open('./subset/relation_subset.data', 'r').read()
relation_subset = eval(o)

relation = []
for u in relation_subset:
	if u[0] in user_dict:
		friend = []
		for f in u[1]:
			if f in user_dict:
				friend.append(user_dict[f])
		relation.append([user_dict[u[0]], friend])

print relation

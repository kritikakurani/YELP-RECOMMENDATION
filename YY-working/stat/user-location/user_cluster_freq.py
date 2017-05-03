import collections
from operator import itemgetter

f = open('location_cluster.data', 'r').read()
location_cluster = eval(f)

clusters = {}
for e in location_cluster:
	clusters[e[0]] = e[1]

f = open('rating_subset_training.data', 'r').read()
rating = eval(f)

res = {}
for r in rating:
	us = r[2]
	bs = r[1]
	if us in res:
		res[us].append(clusters[bs])
	else:
		res[us] = list()
		res[us].append(clusters[bs])

ans = []
for r in res:
	res[r] = collections.Counter(res[r])
	sorted(res[r].items(), key=itemgetter(0))
	count = []
	for k in res[r]:
		count.append([k, res[r][k]])
	ans.append([r, count])

print ans



b = open('labels', 'r').read()
labels = eval(b)

b = open('business_name.data', 'r').read()
business_name = eval(b)

res = {}
for i in xrange(len(labels)):
	lb = labels[i]
	bu = business_name[i]

	if lb in res:
		res[lb].append(bu)
	else: 
		res[lb] = [bu]

ans = []
for r in res:
	ans.append([r, res[r]])

print ans
b = open('labels', 'r').read()
labels = eval(b)

b = open('business_name.data', 'r').read()
business_name = eval(b)

res = []
for i in xrange(len(labels)):
	res.append([business_name[i], labels[i]])

print res
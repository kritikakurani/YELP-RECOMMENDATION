import collections


b = open('location.data', 'r').read()
business = eval(b)

#business,lat,lon,city,state,pcode

state = []
for s in business:
	state.append(s[4])

state = dict(collections.Counter(state))

print state


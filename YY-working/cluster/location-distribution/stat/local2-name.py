
b = open('location.data', 'r').read()
business = eval(b)

name = []
for s in business:
	if s[1] < 35.6 and s[2] > -81.4 and s[2] < -80:
		name.append(str(s[0]))	

print name
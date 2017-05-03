f3 = open('business_5k_name', 'r').read()
business_name = eval(f3)

f4 = open('business_subset.data', 'r').read()
business_subset = eval(f4)

business_avg = [0]*len(business_name)
for b in business_subset:
	if b[0] in business_name:
		business_avg[business_name.index(b[0])] = b[2]

print business_avg
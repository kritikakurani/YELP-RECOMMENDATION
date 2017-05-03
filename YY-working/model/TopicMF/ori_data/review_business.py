f3 = open('business_name.data', 'r').read()
business_name = eval(f3)

f5 = open('rating_subset_training.data', 'r').read()
rating_subset_training = eval(f5)

review_business = []

for r in rating_subset_training:
	review_business.append(business_name.index(r[1]))

print review_business

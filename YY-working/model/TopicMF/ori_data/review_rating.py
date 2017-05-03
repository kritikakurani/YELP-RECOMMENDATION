
f5 = open('rating_subset_training.data', 'r').read()
rating_subset_training = eval(f5)

review_rating = []
for r in rating_subset_training:
	review_rating.append(r[3])

print review_rating

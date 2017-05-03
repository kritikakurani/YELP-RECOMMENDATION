f6 = open('review_subset_training.data', 'r').read()
review_subset_training = eval(f6)

review_txt = []
for r in review_subset_training:
	review_txt.append(r[2])

print review_txt

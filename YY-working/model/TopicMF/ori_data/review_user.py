f1 = open('user_name.data', 'r').read()
user_name = eval(f1)

f5 = open('rating_subset_training.data', 'r').read()
rating_subset_training = eval(f5)

review_user = []

for r in rating_subset_training:
	review_user.append(user_name.index(r[2]))

print review_user

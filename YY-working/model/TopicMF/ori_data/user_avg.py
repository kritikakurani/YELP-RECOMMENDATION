f1 = open('user_5k_name', 'r').read()
user_name = eval(f1)

f2 = open('user_subset.data', 'r').read()
user_subset = eval(f2)

user_avg = [0]*len(user_name)
for u in user_subset:
	if u[0] in user_name:
		user_avg[user_name.index(u[0])] = u[2]

print user_avg
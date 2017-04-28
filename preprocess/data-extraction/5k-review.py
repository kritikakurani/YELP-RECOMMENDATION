
f = open('./5k-data', 'r')
business_name = eval(f.readline())
business_avg = eval(f.readline())
user_name = eval(f.readline())
user_avg = eval(f.readline())

business_dict = {}
for b in xrange(len(business_name)):
	business_dict[business_name[b]] = b

user_dict = {}
for u in xrange(len(user_name)):
	user_dict[user_name[u]] = u

o = open('./subset/rating_subset.data', 'r').read()
rating_subset = eval(o)

o = open('./subset/review_subset.data', 'r').read()
review_subset = eval(o)

review_dict = {}

for r in rating_subset:
	if r[1] in business_dict and r[2] in user_dict:
		review_dict[r[0]] = {}
		review_dict[r[0]]["business"] = business_dict[r[1]]
		review_dict[r[0]]["user"] = user_dict[r[2]]

for r in review_subset:
	if r[0] in review_dict:
		review_dict[r[0]]["rating"] = r[1]
		review_dict[r[0]]["txt"] = r[2]

review_business = []
review_user = []
review_rating = []
review_txt = []

for r in review_dict:
	review_business.append(review_dict[r]["business"])
	review_user.append(review_dict[r]["user"])
	review_rating.append(review_dict[r]["rating"])
	review_txt.append(review_dict[r]["txt"])

print review_business
print review_user
print review_rating
print review_txt



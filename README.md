# YELP-RECOMMENDATION
RECOMMENDATION SYSTEM BASED ON YELP DATA

Youtube Link: https://youtu.be/s6oXCyybIF0
Report: Yelp-final.ipynb

file used from yelp dataset:
yelp_academic_dataset_business.json
yelp_academic_dataset_checkin.json
yelp_academic_dataset_review.json
yelp_academic_dataset_user.json

business.data: all business id, starts, review_count information stored in a list of [business_id, stars, review_count].
business_name.data: all business names used in our project stored in list.
business_subset.data: a subset of business info analyzed in our project, a list of [business_id, stars, review_count].

location.data: all business location information, including business_id, address(street, city, state, postal_code), latitude, longitude.

rating_subset.data: a subset of data used in our project, stored in a list of [review_id, business_id, user_id, stars].
rating_subset_training.data: rating training data used in our project.
rating_subset_test.data: rating testing data used in our project.

relation_subset.data: relationship between yelp users, stored in a list of [user_id, [friend_list]].

review_subset.data: review data related to our project, stored in a list of [review_id, text].
review_subset_training: a subset of review data used for training, same review_id are rating_subset_training.data.

user_name: all user names used in our project stored in list.
user_subset: a subset of users info analyzed in our project, a list of [user_id, review_count, average_stars].

Final Data in ./new_5k
5k-data includes all user information and user average stars and business information and average stars.
5k-reivew includes all review information reviewed_by, reviewed_to, rating and review_text.
5k-relation includes all user and their friends.

packages we used in this project:
random, math, numpy, operator, scipy.sparse, sklearn, scipy.sparse, nltk, stop_word

preprocessing files are in ./preprocess
coding files are in ./bin

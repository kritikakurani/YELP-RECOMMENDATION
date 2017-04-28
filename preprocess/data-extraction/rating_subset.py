import os
import datetime
import json
import re
import math
import numpy as np
import operator
import collections

o = open('business_name.data', 'r').read()
names = eval(o)

file_name = "yelp_academic_dataset_review.json"
path = "./" + file_name
review = []

fInput = open(path,'r')
for line in fInput:
	txt = "[" + line.rstrip() + "]"
	json_txt = json.loads(txt)
	if json_txt[0]["business_id"] in names:
		review.append([json_txt[0]["review_id"], json_txt[0]["business_id"], json_txt[0]["user_id"], json_txt[0]["stars"]])

fInput.close()

print review

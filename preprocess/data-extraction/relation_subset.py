import os
import datetime
import json
import re
import math
import numpy as np
import operator
import collections

o = open('user_name.data', 'r').read()
names = eval(o)

file_name = "yelp_academic_dataset_user.json"
path = "./" + file_name
user = []

fInput = open(path,'r')
for line in fInput:
	txt = "[" + line.rstrip() + "]"
	json_txt = json.loads(txt)
	if json_txt[0]["user_id"] in names:	
		user.append([json_txt[0]["user_id"], json_txt[0]["friends"]])

fInput.close()

print user

import os
import datetime
import json
import re
import math
import numpy as np
import operator
import collections

file_name = "yelp_academic_dataset_business.json"
path = "./" + file_name

business = []

fInput = open(path,'r')
for line in fInput:
	txt = "[" + line.rstrip() + "]"
	json_txt = json.loads(txt)
	business.append([json_txt[0]["business_id"], json_txt[0]["review_count"], json_txt[0]["stars"]])

fInput.close()

print business

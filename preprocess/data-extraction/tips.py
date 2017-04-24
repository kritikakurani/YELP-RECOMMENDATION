import os
import datetime
import json
import re
import math
import numpy as np
import operator
import collections

file_name = "yelp_academic_dataset_tip.json"
path = "./" + file_name

tip = []

fInput = open(path,'r')
for line in fInput:
	txt = "[" + line.rstrip() + "]"
	json_txt = json.loads(txt)
	tip.append([json_txt[0]["business_id"], json_txt[0]["user_id"], json_txt[0]["text"]])

fInput.close()

print tip

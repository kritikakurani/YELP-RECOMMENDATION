import os
import datetime
import json
import re
import math
import numpy as np
import operator
import collections

def loadjason(path, review_count, stars):
    fInput = open(path,'r')
    for line in fInput:
        txt = "[" + line.rstrip() + "]"
        json_txt = json.loads(txt)
        review_count.append(json_txt[0]["review_count"])
        stars.append(json_txt[0]["stars"])
    fInput.close()

file_name = "yelp_academic_dataset_business.json"
path = "./" + file_name

review_count  = list()
stars = list()
loadjason(path, review_count, stars)
user = [review_count, stars]

review_count  = dict(collections.Counter(user[0]))
stars = dict(collections.Counter(user[1]))
user_collections = [review_count, stars]

print user_collections

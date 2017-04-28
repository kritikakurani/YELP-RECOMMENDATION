import os
import datetime
import json
import re
import math
import numpy as np
import operator
import collections

def loadjason(path, review_count, useful, funny, cool, fans, average_stars):
    fInput = open(path,'r')
    for line in fInput:
        txt = "[" + line.rstrip() + "]"
        json_txt = json.loads(txt)
        review_count.append(json_txt[0]["review_count"])
        useful.append(json_txt[0]["useful"])
        funny.append(json_txt[0]["funny"])
        cool.append(json_txt[0]["cool"])
        fans.append(json_txt[0]["fans"])
        average_stars.append(json_txt[0]["average_stars"])
    fInput.close()

file_name = "yelp_academic_dataset_user.json"
path = "./" + file_name

review_count  = list()
useful = list()
funny = list()
cool = list()
fans = list()
average_stars = list()
loadjason(path, review_count, useful, funny, cool, fans, average_stars)
user = [review_count, useful, funny, cool, fans, average_stars]

review_count  = dict(collections.Counter(user[0]))
useful = dict(collections.Counter(user[1]))
funny = dict(collections.Counter(user[2]))
cool = dict(collections.Counter(user[3]))
fans = dict(collections.Counter(user[4]))
average_stars = dict(collections.Counter(user[5]))
user_collections = [review_count, useful, funny, cool, fans, average_stars]

print user_collections

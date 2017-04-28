import numpy as np
import matplotlib.pyplot as plt


o = open('rating_subset.data', 'r').read()
ratings = eval(o)

names = []
for r in ratings:
	names.append(r[2])

names = list(set(names))

print names

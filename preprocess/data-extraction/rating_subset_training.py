import numpy as np
import matplotlib.pyplot as plt


o = open('rating_subset.data', 'r').read()
rating = eval(o)

subset = []
for b in rating[1000:]:
	subset.append(b)

print subset

import numpy as np
import matplotlib.pyplot as plt


o = open('review_subset.data', 'r').read()
review = eval(o)

subset = []
for b in review[1000:]:
	subset.append(b)

print subset

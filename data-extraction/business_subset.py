import numpy as np
import matplotlib.pyplot as plt


o = open('business_name.data', 'r').read()
names = eval(o)

o = open('business.data', 'r').read()
business = eval(o)

subset = []
for b in business:
	if b[0] in names:
		subset.append(b)

print subset

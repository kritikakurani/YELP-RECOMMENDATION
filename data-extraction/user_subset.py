import numpy as np
import matplotlib.pyplot as plt


o = open('user_name.data', 'r').read()
names = eval(o)

o = open('user.data', 'r').read()
user = eval(o)

subset = []
for b in user:
	if b[0] in names:
		subset.append(b)

print subset

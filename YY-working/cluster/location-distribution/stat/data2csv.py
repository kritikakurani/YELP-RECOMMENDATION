import numpy as np
import matplotlib.pyplot as plt


b = open('location.data', 'r').read()
business = eval(b)

print "business,lat,lon,state,pcode"

'''
for s in business:
	print str(s[0]), ",", s[1], ",", s[2], ",", str(s[4]), ",", str(s[5])
	'''

#name = []
for s in business:
	#if s[1] < 35.6 and s[2] > -81.4 and s[2] < -80:
	print str(s[0]), ",", s[1], ",", s[2], ",", str(s[4]), ",", str(s[5])
		#name.append(str(s[0]))	

#print name
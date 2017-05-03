from operator import itemgetter
from collections import Counter
import csv
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from geopy.distance import great_circle
from shapely.geometry import MultiPoint
import matplotlib.cm as cm, matplotlib.font_manager as fm
from datetime import datetime as dt
import time 
from geopy.distance import great_circle

title_font = fm.FontProperties(family='Arial', style='normal', size=20, weight='normal', stretch='normal')
label_font = fm.FontProperties(family='Arial', style='normal', size=16, weight='normal', stretch='normal')
ticks_font = fm.FontProperties(family='Arial', style='normal', size=12, weight='normal', stretch='normal')
annotation_font = fm.FontProperties(family='Arial', style='normal', size=11, weight='normal', stretch='normal')

fig, ax = plt.subplots(figsize=[8, 6])
for label in ax.get_xticklabels():
    label.set_fontproperties(ticks_font)
for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font)
ax.set_xlim([-81.3, -80.4])
ax.set_ylim([34.8, 35.6])
ax.set_title('DBSCAN reduced set', fontproperties=title_font)
ax.set_xlabel('Longitude', fontproperties=label_font)
ax.set_ylabel('Latitude', fontproperties=label_font)



# define the number of kilometers in one radian
kms_per_radian = 6371.0088

in_file = './location-0-3-3-3'
n_flag = 0
epp_list = [0.65, 0.62, 0.6, 0.58, 0.55]

for epp in epp_list:
	print "epp =", epp
	df = pd.read_csv(in_file)
	df.head()
	coords = df.as_matrix(columns=['lat', 'lon'])
	epsilon = epp / kms_per_radian

	start_time = time.time()
	db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
	cluster_labels = db.labels_

	curr = list(Counter(cluster_labels).most_common(1))[0][0]
	labels = list(cluster_labels)


	with open(in_file, 'rb') as f:
		reader = csv.reader(f)
		csv_list = list(reader)

	csv_list2 = [["num","lat","lon"]]
	label_num = len(labels)
	while label_num:
		label_num -= 1
		if labels[label_num] != curr:
			del labels[label_num]
			csv_list2.append(csv_list[label_num+1])
			del csv_list[label_num+1]

	n_flag += 1
	out_file = in_file + '-' + str(n_flag)
	with open(out_file,'wb') as f:
		writer = csv.writer(f)
		writer.writerows(csv_list)
	
	out_file = in_file + '-' + str(n_flag) + '_2'
	with open(out_file,'wb') as f:
		writer = csv.writer(f)
		writer.writerows(csv_list2)

	print "cluster =", len(set(cluster_labels))
	print "restaurant = ", len(csv_list2)
	print "restaurant per cluster = ", 1.0*len(csv_list2)/len(set(cluster_labels))

	rs = pd.read_csv(out_file)
	rs_scatter = ax.scatter(rs['lon'], rs['lat'], c='m', alpha=.7, s=30)
	plt.savefig(out_file)
















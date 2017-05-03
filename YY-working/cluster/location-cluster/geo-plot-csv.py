import pandas as pd, numpy as np, matplotlib.pyplot as plt
import matplotlib.cm as cm, matplotlib.font_manager as fm
from datetime import datetime as dt
from time import time
from shapely.geometry import Polygon
from geopy.distance import great_circle

title_font = fm.FontProperties(family='Arial', style='normal', size=20, weight='normal', stretch='normal')
label_font = fm.FontProperties(family='Arial', style='normal', size=16, weight='normal', stretch='normal')
ticks_font = fm.FontProperties(family='Arial', style='normal', size=12, weight='normal', stretch='normal')
annotation_font = fm.FontProperties(family='Arial', style='normal', size=11, weight='normal', stretch='normal')

ts = pd.read_csv('all_location-centroid.csv')
df = pd.read_csv('all_location.csv')

fig, ax = plt.subplots(figsize=[8, 6])
ts_scatter = ax.scatter(ts['lon'], ts['lat'], c='#99cc99', edgecolor='k', alpha=.7, s=80)
for label in ax.get_xticklabels():
    label.set_fontproperties(ticks_font)
for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font)
ax.set_title('DBSCAN reduced set', fontproperties=title_font)
ax.set_xlabel('Longitude', fontproperties=label_font)
ax.set_ylabel('Latitude', fontproperties=label_font)
plt.savefig("all_location-dbscan-reduce2")

fig, ax = plt.subplots(figsize=[8, 6])
df_scatter = ax.scatter(df['lon'], df['lat'], c='m', edgecolor='k', alpha=.4, s=6)
ts_scatter = ax.scatter(ts['lon'], ts['lat'], c='#99cc99', edgecolor='k', alpha=.7, s=80)
for label in ax.get_xticklabels():
    label.set_fontproperties(ticks_font)
for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font)
ax.set_title('Full data set vs DBSCAN reduced set', fontproperties=title_font)
ax.set_xlabel('Longitude', fontproperties=label_font)
ax.set_ylabel('Latitude', fontproperties=label_font)
ax.legend([df_scatter, ts_scatter], ['Full set', 'Reduced set'], loc='lower right')
plt.savefig("all_location-dbscan-full+reduce2")

'''
rs = pd.read_csv('local2-dbscan-not-0.csv')
fig, ax = plt.subplots(figsize=[8, 6])
rs_scatter = ax.scatter(rs['lon'], rs['lat'], c='#99cc99', edgecolor='k', alpha=.7, s=80)
for label in ax.get_xticklabels():
    label.set_fontproperties(ticks_font)
for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font)
ax.set_title('DBSCAN reduced set', fontproperties=title_font)
ax.set_xlabel('Longitude', fontproperties=label_font)
ax.set_ylabel('Latitude', fontproperties=label_font)
plt.savefig("location-dbscan-reduce-not-0")
'''



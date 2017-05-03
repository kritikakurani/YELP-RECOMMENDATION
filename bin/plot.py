## FOR GRAPH ONLY.
#0.3  y1 = [0.8111237,0.8054977,0.8043302,0.8076009,0.8152823,0.827215,0.8432723,0.863143,0.8865388]
#0.5  y2 = [0.8105134,0.8020313,0.7957705,0.7917243,0.7898928,0.7902676,0.7928506,0.7976021,0.8045191]
#0.1  y3 = [0.8936912,0.9680315,1.0473116,1.1267234,1.2071434,1.2876378,1.3691557,1.4510311,1.5315357]

import math
import matplotlib.pylab as plt
import numpy as np

if True:
    review_count_log = {}
    d1 = {}
    d2 = {}
    d3 = {}
    d4 = {}
    d5 = {}
    d6 = {}
    y1 = [0.804681174, 0.805939185, 0.895384215, 0.858934821, 0.781033057, 0.812830448, 0.826880497, 0.818384015, 0.791903786, 0.816220084]
    y2 = [0.800103783, 0.800694654, 0.888723266, 0.852804478, 0.775533725, 0.807469061, 0.821684175, 0.812887802, 0.786561922, 0.810564921]
    y3 = [0.795308763, 0.793047021, 0.881119122, 0.8529458, 0.768903706, 0.806748773, 0.818007278, 0.812350449, 0.780291122, 0.81001582]
    y4 = [0.787234, 0.792814, 0.872198, 0.833101, 0.767035, 0.796882, 0.810834, 0.805043, 0.774018, 0.804143]
    y5 = [0.772912, 0.777888, 0.855411, 0.821803, 0.75068, 0.791237, 0.790133, 0.790198, 0.758144, 0.790522]
    y6 = [0.867088, 0.87873, 0.967489, 0.942984, 0.862081, 0.86175, 0.905885, 0.883296, 0.868157, 0.899452]
    for n in xrange(len(y)):
        d1[0.1*(n+1)] = y1[n]
        d2[0.1*(n+1)] = y2[n]
        d3[0.1*(n+1)] = y3[n]
        d4[0.1*(n+1)] = y4[n]
        d5[0.1*(n+1)] = y5[n]
        d6[0.1*(n+1)] = y6[n]
    
    lists = sorted(d1.items()) 
    x, y = zip(*lists) 
    plt.plot(x, y)
    lists = sorted(d2.items()) 
    x, y = zip(*lists) 
    plt.plot(x, y)
    lists = sorted(d3.items()) 
    x, y = zip(*lists) 
    plt.plot(x, y)
    lists = sorted(d4.items()) 
    x, y = zip(*lists) 
    plt.plot(x, y)
    lists = sorted(d5.items()) 
    x, y = zip(*lists) 
    plt.plot(x, y) 
    lists = sorted(d6.items()) 
    x, y = zip(*lists) 
    plt.plot(x, y)

    xname = "10-fold"
    yname = "rmse"
    title_name = "10-fold rmse all Models"
    plt.legend(['Ubb','Basic Model','Topic Model', 'Social-Relation Model', 'Social-VIP user Model', 'Social-Similarity Model'], loc='upper right')    
    fig_name = "fig-lbd-10fold"
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.title(title_name)
    plt.savefig(fig_name)
    plt.clf()
    
    

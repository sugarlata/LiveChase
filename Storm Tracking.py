from scipy import misc
import numpy as np
import png
from math import fabs

def find_mean(value_list):
    k = 0.0
    for i in value_list:
        k +=i
    return k/len(value_list)


# Pseudocode

# Load Image

#r = png.Reader("C:\Users\Nathan\Documents\Storm Chasing\\temp\IDR023.T.201112250700.png")

r = png.Reader("C:\Users\Nathan\Documents\Storm Chasing\Chases\\2016-12-21\Radar\IDR023\IDR023.T.201612211100.png")

read = r.read()


# Load into Numpy Array based on intensity 1-16

palette_key_temp = {'(245, 245, 255, 255)': 1,
'(180, 180, 255, 255)': 2,
'(120, 120, 255, 255)': 3,
'(20, 20, 255, 255)': 4,
'(0, 216, 195, 255)': 5,
'(0, 150, 144, 255)': 6,
'(0, 102, 102, 255)': 7,
'(255, 255, 0, 255)': 8,
'(255, 200, 0, 255)': 9,
'(255, 150, 0, 255)': 10,
'(255, 100, 0, 255)': 11,
'(255, 0, 0, 255)': 12,
'(200, 0, 0, 255)': 13,
'(120, 0, 0, 255)': 14,
'(40, 0, 0, 255)': 15}

palette_key_reversed = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}

i_avg = []
for i in range(0,len(read[3]['palette'])):
    for j in palette_key_temp:
        if str(read[3]['palette'][i]) == str(j):
            i_avg.append(i)

i_avg = find_mean(i_avg)

for i in range(0,len(read[3]['palette'])):
    for j in palette_key_temp:
        if str(read[3]['palette'][i]) == str(j):
            if fabs(i-i_avg) < 16:
                palette_key_reversed[palette_key_temp[j]] = i

print
print

pixels_wh = 512

print "Begin"

radar_matrix_init = np.vstack(read[2])

palette_key = dict((v,k) for k,v in palette_key_reversed.iteritems())




from numpy import copy

# Change Radar Intensity to 1-15
radar_matrix_modified = copy(radar_matrix_init)
for k, v in palette_key.iteritems(): radar_matrix_init[radar_matrix_modified == k] = v


# Make everything else zero

radar_matrix_final = np.asarray(radar_matrix_init)
high_values_indices = radar_matrix_final > 15  # Where values are low
low_values_indices = radar_matrix_final < 0  # Where values are low
radar_matrix_final[high_values_indices] = 0  # All low values set to 0
radar_matrix_final[low_values_indices] = 0  # All low values set to 0

x=[]
y=[]
z=[]

radar_matrix_final = np.flipud(radar_matrix_final)

print "Start"
for i in range(0,512):
    for j in range(0,512):
        if radar_matrix_final[i][j] > 4:
            x.append(j)
            y.append(i)
            z.append(radar_matrix_final[i][j])

print "Done"

xi=[]

for i in range(0,len(x)):
    for j in range(0,z[i]):
        xi.append([x[i], y[i]])

X = np.asarray(xi)


from sklearn.cluster import DBSCAN
from sklearn import metrics
from matplotlib import pyplot as plt

from sklearn.cluster import MeanShift, estimate_bandwidth

import collections
from skimage import measure

threshold = 4
radar_matrix_binary = copy(radar_matrix_final)
radar_matrix_binary[radar_matrix_final > threshold] = 1
radar_matrix_binary[radar_matrix_final < threshold + 1] = 0
items = measure.label(radar_matrix_binary)



radar_matrix_binary = copy(items)
radar_matrix_binary[radar_matrix_binary > 0] = 1
radar_matrix_binary[radar_matrix_binary < 1] = 0
items = measure.label(radar_matrix_binary)

biggest = items.ptp()
cluster_skip = []

for i in range(1, biggest + 1):
    print i, (items == i).sum()
    if (items == i).sum() < 60:
        radar_matrix_first = copy(items)
        radar_matrix_binary[radar_matrix_first == i] = 0
        radar_matrix_binary[radar_matrix_binary > 0] = 1

items = measure.label(radar_matrix_binary)

for i in range(1, items.ptp() + 1):
    print i, (items == i).sum()

items = np.flipud(items)

plt.imshow(items, cmap='spectral')

plt.show()





exit()
bandwidth = estimate_bandwidth(X, quantile=0.08, n_samples=100)
print "Start"

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_
print "Finish"

print cluster_centers

labels_unique = np.unique(labels)
if -1 in labels_unique:
    n_clusters_ = len(labels_unique)-1
else:
    n_clusters_ = len(labels_unique)


print len(X)
print len(labels)
print("number of estimated clusters : %d" % n_clusters_)

print X


from itertools import cycle

plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    #plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,markeredgecolor='k', markersize=14)

print my_members
plt.title('Estimated number of clusters: %d' % n_clusters_)


plt.axis([0,512, 0,512])



plt.show()





# Clean Image
# Show image from Numpy Array based on intensity types
#
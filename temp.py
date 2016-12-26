from math import pow
from math import sqrt
import numpy as np

def calc_dist(p1x, p1y, p2x, p2y):
    return sqrt(pow((p1x-p2x),2) + pow((p1y-p2y),2))

points1 = [[121.32603077,262.43138462], [250.26025568,264.60198435], [310.86201459,272.38754189], [93.9226331, 352.73039601], [173.11296115,250.88377408], [301.78787879,487.16666667], [169.30733945,331.69266055], [122.68604651,326.96511628], [498.5, 4.5]]
points2 = [[127.91069036,261.93641154], [261.13153866,260.12235264], [319.30310396,270.80048616], [103.99952347,348.21682154], [185.39177489,244.50577201], [129.72967614,329.69596827], [305.15384615,477.67307692], [180.46153846,324.], [262.5, 310.5], [509.83333333,1.16666667], [230.5, 316.5]]
points3 = [[137.72398904,259.11566885], [266.61441441,260.3016731], [327.18521495,267.60044194], [112.45200893,343.90625], [305.6015625, 470.1875], [198.98605578,236.53984064], [147.01685393,314.45505618], [11.48039216,426.61764706], [196.5, 318.08974359], [367.16666667,179.83333333]]
points4 = [[ 147.35068515,256.94558198], [ 278.48169234,272.54163876], [ 332.99489579,264.56550404], [ 121.85321101,338.3646789 ], [ 164.66494845,303.00412371], [76.55957447,326.72978723], [ 306.97120419,459.19109948], [ 178.88709677,330.91290323], [ 211.85555556,231.32222222], [13.16666667,424.5 ], [ 451.5, 191.5]]
points5 = [[ 155.98544715,259.09138565], [ 289.07003563,268.23401463], [ 133.48804781,336.64661355], [ 343.93980291,261.21122536], [85.51726122,320.83601841], [ 158.56315104,211.359375], [ 225.83846154,228.5 ], [ 309.97747748,457.04054054], [ 194.04545455,322.65909091], [ 326.1, 483.7 ], [ 319.,329.25]]
points6 = [[ 163.14327161,263.40703132], [ 298.94463044,279.52708387], [97.21719457,312.06561086], [ 146.73075953,336.88342165], [ 343.51224596,259.68603439], [ 237.41176471,225.17647059], [ 466.13076923,182.96153846], [76.05555556,353.61111111], [ 418.87837838,204.01351351], [ 333.5, 479.5 ]]

total_points = []
total_totals=[]

# for i in points1:
#     a = []
#     for j in points2:
#         a.append([calc_dist(float(i[0]), float(i[1]), float(j[0]), float(j[1])),[i,j]])
#
#     total_points.append(min(a)[0])
#     total_totals.append(min(a))

for i in points2:
    a = []
    for j in points3:
        a.append([calc_dist(float(i[0]), float(i[1]), float(j[0]), float(j[1])),[i,j]])

    total_points.append(min(a)[0])
    total_totals.append(min(a))
#
# for i in points3:
#     a = []
#     for j in points4:
#         a.append([calc_dist(float(i[0]), float(i[1]), float(j[0]), float(j[1])),[i,j]])
#
#     total_points.append(min(a)[0])
#     total_totals.append(min(a))

# for i in points4:
#     a = []
#     for j in points5:
#         a.append([calc_dist(float(i[0]), float(i[1]), float(j[0]), float(j[1])),[i,j]])
#
#     total_points.append(min(a)[0])
#     total_totals.append(min(a))
#
# for i in points5:
#     a = []
#     for j in points6:
#         a.append([calc_dist(float(i[0]), float(i[1]), float(j[0]), float(j[1])),[i,j]])
#
#     total_points.append(min(a)[0])
#     total_totals.append(min(a))

for i in total_points:
    print i

distance = np.asarray(total_points)
print "STD DEV"
std = distance.std()

while std > 10:
    max_dist_matrix = distance < max(distance)
    distance = distance[max_dist_matrix]
    print
    std = distance.std()
    print std
    print distance

for i in distance:
    print i

for i in total_totals:
    print i



print
print distance
print total_totals
print "Total Totals"

from matplotlib import pyplot as plt

ax = plt.axes()

for i in total_totals:
    if i[0] in distance:
        print
        print "Match:"
        print i[1][0], i[1][1]

        ax.arrow(i[1][0][0],i[1][0][1], i[1][1][0]-i[1][0][0], i[1][1][1]-i[1][0][1], head_width=10, head_length=20)


plt.axis([0,512, 0,512])

x=[]
y=[]
for i in points2:
    x.append(i[0])
    y.append(i[1])

ax.scatter(x,y)
plt.show()



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def SaveFigureAsImage(fileName, fig=None, **kwargs):
    ''' Save a Matplotlib figure as an image without borders or frames.
       Args:
            fileName (str): String that ends in .png etc.

            fig (Matplotlib figure instance): figure you want to save as the image
        Keyword Args:
            orig_size (tuple): width, height of the original image used to maintain
            aspect ratio.
    '''

    fig_size = fig.get_size_inches()
    w, h = fig_size[0], fig_size[1]
    fig.patch.set_alpha(0)
    if kwargs.has_key('orig_size'):  # Aspect ratio scaling if required
        w, h = kwargs['orig_size']
        w2, h2 = fig_size[0], fig_size[1]
        fig.set_size_inches([(w2 / w) * w, (w2 / w) * h])
        fig.set_dpi((w2 / w) * fig.get_dpi())
    a = fig.gca()
    a.set_frame_on(False)
    a.set_xticks([]);
    a.set_yticks([])
    # plt.axis('off')
    # plt.xlim(-44, -33);
    # plt.ylim(139, 151)
    fig.savefig(fileName, transparent=True, bbox_inches='tight', \
                pad_inches=0, dpi=400)







# import numpy as np
print "begin import matplotlib"
import matplotlib.pyplot as plt
print "finished"
#
# xlist = np.linspace(-3.0,3.0,50)
# ylist = np.linspace(-3.0,3.0,50)
#
# X, Y = np.meshgrid(xlist,ylist)
#
# Z = np.sqrt(X**2 + Y**2)
#
# print Z
#
# plt.figure()
#
# cp = plt.contour(X,Y,Z)
#
# plt.clabel(cp, inline=True,fontsize=10)
# plt.title('Contour Plot')
# plt.xlabel('x cm')
# plt.ylabel('y cm')
#
# plt.show()

#
# from numpy import linspace, meshgrid
# from matplotlib.mlab import griddata
#
# def grid(x, y, z, resX=100, resY=100):
#     "Convert 3 column data to matplotlib grid"
#     xi = linspace(min(x), max(x), resX)
#     yi = linspace(min(y), max(y), resY)
#     Z = griddata(x, y, z, xi, yi, interp='cubic')
#     X, Y = meshgrid(xi, yi)
#     return X, Y, Z
#

print "egin imports"
import Download_Observations
print "mid import"
import numpy
print "end imports"

print "Get Data"
obs_list = Download_Observations.give_me_vic_obs()
print "Got Data"
print

x=[]
y=[]
z=[]

for i in range(0,len(obs_list)):
    if obs_list[i].dew == "-":
        continue

    y.append(obs_list[i].lat)
    x.append(obs_list[i].lon)
    print
    print obs_list[i].loc_name
    print obs_list[i].dew
    z.append(obs_list[i].dew)

#x=[0,0,0,2,2,3,3,3,1.5,1,1.75,2,2]
#y=[1,3,5,1,3,4,5,1,3,2,3,3.75,3.35]
#z=[5,2,1,4,2,5,8,0,2,3,2.5,2.5,2.5]

resolution = 100

print "Do a little math"

# http://www.python-course.eu/matplotlib_contour_plot.php
# http://cgcooke.github.io/Scattered-Interpolation/

#
# X, Y, Z = grid(x, y, z)
# plt.contourf(X, Y, Z)
#
# plt.show()
#


from scipy.interpolate import griddata

w=int(750)
h=int(625)

xi = np.linspace(141,150,resolution)
yi = np.linspace(-39,-34,resolution)
# grid the data.
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')

w=15
h=12.5


fig = plt.figure(figsize=(w,h),facecolor='w',frameon=False,edgecolor="Yellow")

ax = fig.add_subplot(111)



ax.contourf(xi,yi,zi,15,cmap=plt.cm.jet)

ax.scatter(x,y,marker='o',c='b',s=.1)

ax.axis([141,150,-39,-34])

ax.set_axis_off()
fig.subplots_adjust(left=0, right=1,bottom=0,top=1,hspace=0,wspace=0)
#fig.margins(0,0)
#ax.xaxis.set_major_locator(NullLocator())


fig.tight_layout(pad=0)

print "Start Save"
SaveFigureAsImage("C:\\Users\\Nathan\\Documents\\Development\\LiveChase\\LiveChase\\fig3.png",fig=fig)
#fig.savefig("C:\\Users\\Nathan\\Documents\\Development\\LiveChase\\LiveChase\\fig3.png",bbox_inches='tight',dpi=200, pad_inches=0.0, transparent=True)
print "End Save"










exit()
print "begin imports"
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import numpy.ma as ma
from numpy.random import uniform, seed
print "end imports"

#seed(1234)
npts = len(x)
# x = uniform(-2,2,npts)
# y = uniform(-2,2,npts)
# z = x*np.exp(-x**2-y**2)
# define grid.

w=int(750)
h=int(625)

xi = np.linspace(139,151,resolution)
yi = np.linspace(-43,-33,resolution)
# grid the data.
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
# contour the gridded data, plotting dots at the randomly spaced data points.

buf = plt.rcParams.keys()

for i in buf:
    print i

plt.rcParams['figure.figsize'] = w, h
plt.rcParams['savefig.dpi'] = 100

plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
#C = plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')

#plt.clabel(C, inline=1, fontsize=6)

plt.xticks(())
plt.yticks(())


print
print "Begin Save"

#plt.tight_layout(0)
plt.show()
plt.savefig("C:\\Users\\Nathan\\Documents\\Development\\LiveChase\\LiveChase\\fig.png")

print "Begin Second Save"
fig = plt.figure(figsize=(750,625))

ax = fig.add_subplot(111)


fig.savefig("C:\\Users\\Nathan\\Documents\\Development\\LiveChase\\LiveChase\\fig2.png", dpi=199)

exit()

plt.colorbar() # draw colorbar
# plot data points.
plt.scatter(x,y,marker='o',c='b',s=5)
plt.xlim(min(x),max(x))
plt.ylim(min(y),max(y))
plt.title('griddata test (%d points)' % npts)


plt.show()


exit()


fig = plt.figure(frameon=False)
fig.set_size_inches(w,h)
ax = plt.Axes(fig, [0.,0.,1.,1.,])
ax.set_axis_off()
fig.add_axes(ax)
ax.imshow(numpy.random.rand(h,w), aspect='normal')
fig.savefig("C:\\Users\\Nathan\\Documents\\Development\\LiveChase\\LiveChase\\fig.png", dpi=1)



#plt.show()
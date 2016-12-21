print "Begin Imports"
from arrow import get as arrow_get
from arrow import now as arrow_now
from arrow import parser
first_time = arrow_now().timestamp
from Download_Observations import give_me_vic_obs
from Download_Observations import give_me_full_obs
from Download_Observations import ObservationLocation
from Create_KML_Observations import create_vic_obs_points
from Create_KML_Observations import create_vic_overlays
from datetime import datetime
from matplotlib import pyplot as plt
from os import remove as os_remove
from os import listdir
from re import match as re_match
from scipy.interpolate import griddata
from numpy import linspace
from pprint import pprint
print "End Imports"

class ProcessObs:

    obs_list = []
    loc_names = []

    def __init__(self):
        self.obs_list, self.loc_names = give_me_vic_obs()
    def update_observations(self):

        self.obs_list, self.loc_names = give_me_vic_obs()

    def SaveFigureAsImage(self, fileName, fig=None, **kwargs):
        ''' Save a Matplotlib figure as an image without borders or frames.
           Args:
                fileName (str): String that ends in .png etc.

                fig (Matplotlib figure instance): figure you want to save as the image
            Keyword Args:
                orig_size (tuple): width, height of the original image used to maintain
                aspect ratio.
        '''

        fig_size = fig.get_size_inches()
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
        fig.savefig(fileName, transparent=True, bbox_inches='tight', pad_inches=0, dpi=100)

    def create_current_obs_graphs(self):

        location_objects = []

        for i in range(0, len(self.loc_names)):

            root_folder = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\"
            date_path = arrow_now().format('YYYY-MM-DD')

            for j in range(0, len(self.obs_list)):
                if self.loc_names[i] == self.obs_list[j].code:

                    code = self.obs_list[j].code
                    loc_name = self.obs_list[j].loc_name
                    lat = self.obs_list[j].lat
                    lon = self.obs_list[j].lon
                    height = self.obs_list[j].height
                    break
            with open(root_folder + date_path + "\Observations\\" + self.loc_names[i] + ".csv") as f:
                for line in f:
                    line = line.split(',')
                    location_objects.append(ObservationLocation(code, loc_name, lat, lon, height))
                    location_objects[len(location_objects) - 1].time = line[0]
                    location_objects[len(location_objects) - 1].temp = line[1]
                    location_objects[len(location_objects) - 1].dew = line[2]
                    location_objects[len(location_objects) - 1].rain = line[3]
                    location_objects[len(location_objects) - 1].pressure = line[4]
                    location_objects[len(location_objects) - 1].lcl = line[5]
                    location_objects[len(location_objects) - 1].rel_hum = line[6]
                    location_objects[len(location_objects) - 1].wind_vel = line[7]
                    location_objects[len(location_objects) - 1].wind_dir = str(line[8]).replace('\n','')

        print
        t = 0
        for k in self.loc_names:

            loc_obs_temp = []
            loc_obs_dew = []
            loc_obs_rain = []
            loc_obs_pressure = []
            loc_obs_lcl = []
            loc_obs_rel_hum = []
            loc_obs_wind_vel = []
            loc_obs_wind_dir = []

            dpi_int = 50

            for j in location_objects:

                if k == j.code:
                    loc_obs_temp.append([j.time, j.temp])
                    loc_obs_dew.append([j.time, j.dew])
                    loc_obs_rain.append([j.time, j.rain])
                    loc_obs_pressure.append([j.time, j.pressure])
                    loc_obs_lcl.append([j.time, j.lcl])
                    loc_obs_rel_hum.append([j.time, j.rel_hum])
                    loc_obs_wind_vel.append([j.time, j.wind_vel])
                    loc_obs_wind_dir.append([j.time, j.wind_dir])

            if True:
                print
                print str(int(round(100 * float(t) / float(len(self.loc_names)), 0))) + "% Done"

                t += 1
                print "Beginning to create graphs for", k
                if len(loc_obs_temp) > 1:

                    # Code to create graphs go here.

                    # Create temperature graph first


                    graph_type = "temperature"

                    file_short_list = []
                    for f in listdir(root_folder + date_path + "\Observations\\"):
                        if re_match(k + "-" + graph_type, f):
                            file_short_list.append(f)
                    if len(file_short_list) > 1:
                        file_short_list.sort()
                        file_short_list.remove(file_short_list[-1])
                        for g in file_short_list:
                            os_remove(root_folder + date_path + "\Observations\\" + g)

                    print "Creating", graph_type, "graph"

                    x = []
                    y = []

                    for m in loc_obs_temp:
                        try:
                            y.append(float(m[1]))
                            x.append(datetime.fromtimestamp(float(m[0])))
                        except ValueError:
                            continue
                    try:
                        time_now = arrow_get(x[len(x) - 1]).format('HH-mm')
                    except IndexError:
                        continue

                    try:
                        with open(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png"):
                            print "Graph Already Exists"
                    except IOError:

                        fig = plt.figure(figsize=(16, 9))

                        ax = fig.add_subplot(111)
                        ax.plot(x, y)

                        for xy in zip(x, y):
                            ax.annotate(xy[1], xy=xy, textcoords='data')

                        buf = (max(y) - min(y)) * .1
                        ax.get_yaxis().get_major_formatter().set_useOffset(False)
                        ax.axis([x[0], x[len(x) - 1], min(y) - buf, max(y) + buf])

                        fig.tight_layout(pad=3)
                        print "Saving"
                        plt.savefig(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png", dpi=dpi_int, )
                        plt.close()


                    # Create dew points graph

                    graph_type = "dew-point"

                    file_short_list = []
                    for f in listdir(root_folder + date_path + "\Observations\\"):
                        if re_match(k + "-" + graph_type, f):
                            file_short_list.append(f)
                    if len(file_short_list) > 1:
                        file_short_list.sort()
                        file_short_list.remove(file_short_list[-1])
                        for g in file_short_list:
                            os_remove(root_folder + date_path + "\Observations\\" + g)

                    print "Creating", graph_type, "graph"

                    x = []
                    y = []

                    for m in loc_obs_dew:
                        try:
                            y.append(float(m[1]))
                            x.append(datetime.fromtimestamp(float(m[0])))
                        except ValueError:
                            continue
                    try:
                        time_now = arrow_get(x[len(x) - 1]).format('HH-mm')
                    except IndexError:
                        continue

                    try:
                        with open(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png"):
                            print "Graph Already Exists"
                    except IOError:
                        fig = plt.figure(figsize=(16, 9))

                        ax = fig.add_subplot(111)
                        ax.plot(x, y)

                        for xy in zip(x, y):
                            ax.annotate(xy[1], xy=xy, textcoords='data')

                        buf = (max(y) - min(y)) * .1
                        ax.get_yaxis().get_major_formatter().set_useOffset(False)
                        ax.axis([x[0], x[len(x) - 1], min(y) - buf, max(y) + buf])

                        fig.tight_layout(pad=3)
                        print "Saving"
                        plt.savefig(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png", dpi=dpi_int)
                        plt.close()

                    # Create rain points graph

                    graph_type = "rain"

                    file_short_list = []
                    for f in listdir(root_folder + date_path + "\Observations\\"):
                        if re_match(k + "-" + graph_type, f):
                            file_short_list.append(f)
                    if len(file_short_list) > 1:
                        file_short_list.sort()
                        file_short_list.remove(file_short_list[-1])
                        for g in file_short_list:
                            os_remove(root_folder + date_path + "\Observations\\" + g)

                    print "Creating", graph_type, "graph"

                    x = []
                    y = []

                    for m in loc_obs_rain:
                        try:
                            y.append(float(m[1]))
                            x.append(datetime.fromtimestamp(float(m[0])))
                        except ValueError:
                            continue
                    try:
                        time_now = arrow_get(x[len(x) - 1]).format('HH-mm')
                    except IndexError:
                        continue

                    try:
                        with open(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png"):
                            print "Graph Already Exists"
                    except IOError:
                        fig = plt.figure(figsize=(16, 9))

                        ax = fig.add_subplot(111)
                        ax.plot(x, y)

                        for xy in zip(x, y):
                            ax.annotate(xy[1], xy=xy, textcoords='data')

                        buf = (max(y) - min(y)) * .1
                        ax.get_yaxis().get_major_formatter().set_useOffset(False)
                        ax.axis([x[0], x[len(x) - 1], min(y) - buf, max(y) + buf])

                        fig.tight_layout(pad=3)
                        print "Saving"
                        plt.savefig(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png", dpi=dpi_int)
                        plt.close()

                    # Create Pressure Graph

                    graph_type = "pressure"

                    file_short_list = []
                    for f in listdir(root_folder + date_path + "\Observations\\"):
                        if re_match(k + "-" + graph_type, f):
                            file_short_list.append(f)
                    if len(file_short_list) > 1:
                        file_short_list.sort()
                        file_short_list.remove(file_short_list[-1])
                        for g in file_short_list:
                            os_remove(root_folder + date_path + "\Observations\\" + g)

                    print "Creating", graph_type, "graph"

                    x = []
                    y = []

                    for m in loc_obs_pressure:
                        try:
                            y.append(float(m[1]))
                            x.append(datetime.fromtimestamp(float(m[0])))
                        except ValueError:
                            continue
                    try:
                        time_now = arrow_get(x[len(x)-1]).format('HH-mm')
                    except IndexError:
                        continue

                    try:
                        with open(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png"):
                            print "Graph Already Exists"
                    except IOError:
                        fig = plt.figure(figsize=(16,9))

                        ax = fig.add_subplot(111)
                        ax.plot(x,y)

                        for xy in zip(x, y):
                            ax.annotate(xy[1], xy=xy, textcoords='data')

                        buf = (max(y)-min(y))*.1
                        ax.get_yaxis().get_major_formatter().set_useOffset(False)
                        ax.axis([x[0], x[len(x)-1],min(y)-buf,max(y)+buf])

                        fig.tight_layout(pad=3)
                        print "Saving"
                        plt.savefig(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png", dpi=dpi_int)
                        plt.close()

                    # Create LCL Graph


                    graph_type = "lcl"

                    file_short_list = []
                    for f in listdir(root_folder + date_path + "\Observations\\"):
                        if re_match(k + "-" + graph_type, f):
                            file_short_list.append(f)
                    if len(file_short_list) > 1:
                        file_short_list.sort()
                        file_short_list.remove(file_short_list[-1])
                        for g in file_short_list:
                            os_remove(root_folder + date_path + "\Observations\\" + g)

                    print "Creating", graph_type, "graph"

                    x = []
                    y = []

                    for m in loc_obs_lcl:
                        try:
                            y.append(float(m[1]))
                            x.append(datetime.fromtimestamp(float(m[0])))
                        except ValueError:
                            continue
                    try:
                        time_now = arrow_get(x[len(x) - 1]).format('HH-mm')
                    except IndexError:
                        continue

                    try:
                        with open(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png"):
                            print "Graph Already Exists"
                    except IOError:
                        fig = plt.figure(figsize=(16,9))

                        ax = fig.add_subplot(111)
                        ax.plot(x,y)

                        for xy in zip(x, y):
                            ax.annotate(xy[1], xy=xy, textcoords='data')

                        buf = (max(y)-min(y))*.1
                        ax.get_yaxis().get_major_formatter().set_useOffset(False)
                        ax.axis([x[0], x[len(x)-1],min(y)-buf,max(y)+buf])

                        fig.tight_layout(pad=3)
                        print "Saving"
                        plt.savefig(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png", dpi=dpi_int)
                        plt.close()

                    # Create relative humidity Graph

                    graph_type = "rel_hum"

                    file_short_list = []
                    for f in listdir(root_folder + date_path + "\Observations\\"):
                        if re_match(k + "-" + graph_type, f):
                            file_short_list.append(f)
                    if len(file_short_list) > 1:
                        file_short_list.sort()
                        file_short_list.remove(file_short_list[-1])
                        for g in file_short_list:
                            os_remove(root_folder + date_path + "\Observations\\" + g)

                    print "Creating", graph_type, "graph"

                    x = []
                    y = []

                    for m in loc_obs_rel_hum:
                        try:
                            y.append(float(m[1]))
                            x.append(datetime.fromtimestamp(float(m[0])))
                        except ValueError:
                            continue
                    try:
                        time_now = arrow_get(x[len(x) - 1]).format('HH-mm')
                    except IndexError:
                        continue

                    try:
                        with open(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png"):
                            print "Graph Already Exists"
                    except IOError:
                        fig = plt.figure(figsize=(16,9))

                        ax = fig.add_subplot(111)
                        ax.plot(x,y)

                        for xy in zip(x, y):
                            ax.annotate(xy[1], xy=xy, textcoords='data')

                        buf = (max(y)-min(y))*.1
                        ax.get_yaxis().get_major_formatter().set_useOffset(False)
                        ax.axis([x[0], x[len(x)-1],min(y)-buf,max(y)+buf])

                        fig.tight_layout(pad=3)
                        print "Saving"
                        plt.savefig(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png", dpi=dpi_int)
                        plt.close()

                    # Create wind speed graph

                    graph_type = "wind"

                    file_short_list = []
                    for f in listdir(root_folder + date_path + "\Observations\\"):
                        if re_match(k + "-" + graph_type, f):
                            file_short_list.append(f)
                    if len(file_short_list) > 1:
                        file_short_list.sort()
                        file_short_list.remove(file_short_list[-1])
                        for g in file_short_list:
                            os_remove(root_folder + date_path + "\Observations\\" + g)

                    print "Creating", graph_type, "graph"

                    x = []
                    y = []

                    for m in loc_obs_wind_vel:
                        try:
                            y.append(float(m[1]))
                            x.append(datetime.fromtimestamp(float(m[0])))
                        except ValueError:
                            continue
                    try:
                        time_now = arrow_get(x[len(x) - 1]).format('HH-mm')
                    except IndexError:
                        continue

                    try:
                        with open(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png"):
                            print "Graph Already Exists"
                    except IOError:
                        fig = plt.figure(figsize=(16,9))

                        ax = fig.add_subplot(111)
                        ax.plot(x,y)

                        for xy in zip(x, y):
                            ax.annotate(xy[1], xy=xy, textcoords='data')

                        buf = (max(y)-min(y))*.1
                        ax.get_yaxis().get_major_formatter().set_useOffset(False)
                        ax.axis([x[0], x[len(x)-1],min(y)-buf,max(y)+buf])

                        fig.tight_layout(pad=3)
                        print "Saving"
                        plt.savefig(root_folder + date_path + "\Observations\\" + k + "-" + graph_type + "-" + time_now + ".png", dpi=dpi_int)
                        plt.close()


    def create_current_overlays(self):

        root_folder = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\"
        date_path = arrow_now().format('YYYY-MM-DD')

        config_filename = root_folder + date_path + "\Observations\\" + "range.cfg"

        min_temp = "-"
        max_temp = "-"
        min_dew = "-"
        max_dew = "-"
        min_pressure = "-"
        max_pressure = "-"
        min_rain = "-"
        max_rain = "-"
        min_rel_hum = "-"
        max_rel_hum = "-"
        min_lcl = "-"
        max_lcl = "-"
        min_wind_vel = "-"
        max_wind_vel = "-"
        
        with open(config_filename, 'r') as f:
            line = f.readline()
            line_list = line.split(',')
            min_temp = float(line_list[0])
            max_temp = float(line_list[1].replace('\n',''))

            line = f.readline()
            line_list = line.split(',')
            min_dew = float(line_list[0])
            max_dew = float(line_list[1].replace('\n', ''))

            line = f.readline()
            line_list = line.split(',')
            min_rain = float(line_list[0])
            max_rain = float(line_list[1].replace('\n', ''))
    
            line = f.readline()
            line_list = line.split(',')
            min_pressure = float(line_list[0])
            max_pressure = float(line_list[1].replace('\n', ''))
    
            line = f.readline()
            line_list = line.split(',')
            min_rel_hum = float(line_list[0])
            max_rel_hum = float(line_list[1].replace('\n', ''))
    
            line = f.readline()
            line_list = line.split(',')
            min_lcl = float(line_list[0])
            max_lcl = float(line_list[1].replace('\n', ''))
    
            line = f.readline()
            line_list = line.split(',')
            min_wind_vel = float(line_list[0])
            max_wind_vel = float(line_list[1].replace('\n', ''))
        print
        
        # Temperature Graph
        if True:
            graph_type = "temp"

            time_now = arrow_get(self.obs_list[36].time, 'HH:mmA').format('HH-mm')
            graph_filename = root_folder + date_path + "\Observations\\" + "vic-" + graph_type + "-" + time_now + ".png"

            try:
                with open(graph_filename, 'r') as f:
                    print "Graph already created"
            except IOError:
                x = []
                y = []
                z = []
                for i in range(0, len(self.obs_list)):
                    if self.obs_list[i].temp == "-":
                        continue
                    y.append(self.obs_list[i].lat)
                    x.append(self.obs_list[i].lon)
                    z.append(self.obs_list[i].temp)
                resolution = 100
                xi = linspace(141, 150, resolution)
                yi = linspace(-39, -34, resolution)
                zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')
                print min(z), max(z)
                w = 15
                h = 12.5
                fig = plt.figure(figsize=(w, h), facecolor='w', frameon=False, edgecolor="Yellow")
                ax = fig.add_subplot(111)
                ax.contourf(xi, yi, zi, 120, cmap=plt.cm.jet, vmin=min_temp,vmax=max_temp)
                C = ax.contour(xi, yi, zi, 20, linewidths=0.5, colors='k')
                ax.clabel(C, inline=1, fontsize=6, fmt='%1.0f')
                ax.scatter(x, y, marker='o', c='b', s=.1)
                ax.axis([141, 150, -39, -34])
                ax.set_axis_off()
                fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)
                fig.tight_layout(pad=0)

                print "Start Save for", graph_type
                print graph_filename
                self.SaveFigureAsImage(graph_filename, fig=fig)
                print "End Save"

        # Dew Point Graph
        if True:
            graph_type = "dew"

            time_now = arrow_get(self.obs_list[36].time, 'HH:mmA').format('HH-mm')
            graph_filename = root_folder + date_path + "\Observations\\" + "vic-" + graph_type + "-" + time_now + ".png"

            try:
                with open(graph_filename, 'r') as f:
                    print "Graph already created"
            except IOError:
                x = []
                y = []
                z = []
                for i in range(0, len(self.obs_list)):
                    if self.obs_list[i].dew == "-":
                        continue
                    y.append(self.obs_list[i].lat)
                    x.append(self.obs_list[i].lon)
                    z.append(self.obs_list[i].dew)
                resolution = 100
                xi = linspace(141, 150, resolution)
                yi = linspace(-39, -34, resolution)
                zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')
                w = 15
                h = 12.5
                fig = plt.figure(figsize=(w, h), facecolor='w', frameon=False, edgecolor="Yellow")
                ax = fig.add_subplot(111)
                ax.contourf(xi, yi, zi, 15, cmap=plt.cm.jet, vmin=min_dew, vmax=max_dew)
                C = ax.contour(xi, yi, zi, 20, linewidths=0.5, colors='k')
                ax.clabel(C, inline=1, fontsize=6, fmt='%1.0f')
                ax.scatter(x, y, marker='o', c='b', s=.1)
                ax.axis([141, 150, -39, -34])
                ax.set_axis_off()
                fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)
                fig.tight_layout(pad=0)

                print "Start Save for", graph_type
                print graph_filename
                self.SaveFigureAsImage(graph_filename, fig=fig)
                print "End Save"

        # Rain Graph
        if True:
            graph_type = "rain"

            time_now = arrow_get(self.obs_list[36].time, 'HH:mmA').format('HH-mm')
            graph_filename = root_folder + date_path + "\Observations\\" + "vic-" + graph_type + "-" + time_now + ".png"

            try:
                with open(graph_filename, 'r') as f:
                    print "Graph already created"
            except IOError:
                x = []
                y = []
                z = []
                for i in range(0, len(self.obs_list)):
                    if self.obs_list[i].rain == "-":
                        continue
                    y.append(self.obs_list[i].lat)
                    x.append(self.obs_list[i].lon)
                    z.append(self.obs_list[i].rain)
                resolution = 100
                xi = linspace(141, 150, resolution)
                yi = linspace(-39, -34, resolution)
                zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')
                w = 15
                h = 12.5
                fig = plt.figure(figsize=(w, h), facecolor='w', frameon=False, edgecolor="Yellow")
                ax = fig.add_subplot(111)
                ax.contourf(xi, yi, zi, 15, cmap=plt.cm.jet, vmin=min_rain, vmax=max_rain)
                C = ax.contour(xi, yi, zi, 20, linewidths=0.5, colors='k')
                ax.clabel(C, inline=1, fontsize=6, fmt='%1.0f')
                ax.scatter(x, y, marker='o', c='b', s=.1)
                ax.axis([141, 150, -39, -34])
                ax.set_axis_off()
                fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)
                fig.tight_layout(pad=0)

                print "Start Save for", graph_type
                print graph_filename
                self.SaveFigureAsImage(graph_filename, fig=fig)
                print "End Save"

        # Pressure Point Graph
        if True:
            graph_type = "pressure"

            time_now = arrow_get(self.obs_list[36].time, 'HH:mmA').format('HH-mm')
            graph_filename = root_folder + date_path + "\Observations\\" + "vic-" + graph_type + "-" + time_now + ".png"

            try:
                with open(graph_filename, 'r') as f:
                    print "Graph already created"
            except IOError:
                x = []
                y = []
                z = []
                for i in range(0, len(self.obs_list)):
                    if self.obs_list[i].pressure == "-":
                        continue
                    y.append(self.obs_list[i].lat)
                    x.append(self.obs_list[i].lon)
                    z.append(self.obs_list[i].pressure)
                resolution = 100
                xi = linspace(141, 150, resolution)
                yi = linspace(-39, -34, resolution)
                zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')
                w = 15
                h = 12.5
                fig = plt.figure(figsize=(w, h), facecolor='w', frameon=False, edgecolor="Yellow")
                ax = fig.add_subplot(111)
                ax.contourf(xi, yi, zi, 15, cmap=plt.cm.jet, vmin=min_pressure, vmax=max_pressure)
                C = ax.contour(xi, yi, zi, 20, linewidths=0.5, colors='k')
                ax.clabel(C, inline=1, fontsize=6, fmt='%1.0f')
                ax.scatter(x, y, marker='o', c='b', s=.1)
                ax.axis([141, 150, -39, -34])
                ax.set_axis_off()
                fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)
                fig.tight_layout(pad=0)

                print "Start Save for", graph_type
                print graph_filename
                self.SaveFigureAsImage(graph_filename, fig=fig)
                print "End Save"

        # Relative Humidity Graph
        if True:
            graph_type = "rel_hum"

            time_now = arrow_get(self.obs_list[36].time, 'HH:mmA').format('HH-mm')
            graph_filename = root_folder + date_path + "\Observations\\" + "vic-" + graph_type + "-" + time_now + ".png"

            try:
                with open(graph_filename, 'r') as f:
                    print "Graph already created"
            except IOError:
                x = []
                y = []
                z = []
                for i in range(0, len(self.obs_list)):
                    if self.obs_list[i].rel_hum == "-":
                        continue
                    y.append(self.obs_list[i].lat)
                    x.append(self.obs_list[i].lon)
                    z.append(self.obs_list[i].rel_hum)
                resolution = 100
                xi = linspace(141, 150, resolution)
                yi = linspace(-39, -34, resolution)
                zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')
                w = 15
                h = 12.5
                fig = plt.figure(figsize=(w, h), facecolor='w', frameon=False, edgecolor="Yellow")
                ax = fig.add_subplot(111)
                ax.contourf(xi, yi, zi, 15, cmap=plt.cm.jet, vmin=min_rel_hum, vmax=max_rel_hum)
                C = ax.contour(xi, yi, zi, 20, linewidths=0.5, colors='k')
                ax.clabel(C, inline=1, fontsize=6, fmt='%1.0f')
                ax.scatter(x, y, marker='o', c='b', s=.1)
                ax.axis([141, 150, -39, -34])
                ax.set_axis_off()
                fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)
                fig.tight_layout(pad=0)

                print "Start Save for", graph_type
                print graph_filename
                self.SaveFigureAsImage(graph_filename, fig=fig)
                print "End Save"

        # LCL Graph
        if True:
            graph_type = "lcl"

            time_now = arrow_get(self.obs_list[36].time, 'HH:mmA').format('HH-mm')
            graph_filename = root_folder + date_path + "\Observations\\" + "vic-" + graph_type + "-" + time_now + ".png"

            try:
                with open(graph_filename, 'r') as f:
                    print "Graph already created"
            except IOError:
                x = []
                y = []
                z = []
                for i in range(0, len(self.obs_list)):
                    if self.obs_list[i].lcl == "-":
                        continue
                    y.append(self.obs_list[i].lat)
                    x.append(self.obs_list[i].lon)
                    z.append(self.obs_list[i].lcl)
                resolution = 100
                xi = linspace(141, 150, resolution)
                yi = linspace(-39, -34, resolution)
                zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')
                w = 15
                h = 12.5
                fig = plt.figure(figsize=(w, h), facecolor='w', frameon=False, edgecolor="Yellow")
                ax = fig.add_subplot(111)
                ax.contourf(xi, yi, zi, 15, cmap=plt.cm.jet, vmin=min_lcl, vmax=max_lcl)
                C = ax.contour(xi, yi, zi, 20, linewidths=0.5, colors='k')
                ax.clabel(C, inline=1, fontsize=6, fmt='%1.0f')
                ax.scatter(x, y, marker='o', c='b', s=.1)
                ax.axis([141, 150, -39, -34])
                ax.set_axis_off()
                fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)
                fig.tight_layout(pad=0)

                print "Start Save for", graph_type
                print graph_filename
                self.SaveFigureAsImage(graph_filename, fig=fig)
                print "End Save"

        # Wind Graph
        if True:
            graph_type = "wind_vel"

            time_now = arrow_get(self.obs_list[36].time, 'HH:mmA').format('HH-mm')
            graph_filename = root_folder + date_path + "\Observations\\" + "vic-" + graph_type + "-" + time_now + ".png"

            try:
                with open(graph_filename, 'r') as f:
                    print "Graph already created"
            except IOError:
                x = []
                y = []
                z = []
                for i in range(0, len(self.obs_list)):
                    if self.obs_list[i].wind_vel == "-":
                        continue
                    y.append(self.obs_list[i].lat)
                    x.append(self.obs_list[i].lon)
                    z.append(self.obs_list[i].wind_vel)
                resolution = 100
                xi = linspace(141, 150, resolution)
                yi = linspace(-39, -34, resolution)
                zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')
                w = 15
                h = 12.5
                fig = plt.figure(figsize=(w, h), facecolor='w', frameon=False, edgecolor="Yellow")
                ax = fig.add_subplot(111)
                ax.contourf(xi, yi, zi, 15, cmap=plt.cm.jet, vmin=min_wind_vel, vmax=max_wind_vel)
                C = ax.contour(xi, yi, zi, 20, linewidths=0.5, colors='k')
                ax.clabel(C, inline=1, fontsize=6, fmt='%1.0f')
                ax.scatter(x, y, marker='o', c='b', s=.1)
                ax.axis([141, 150, -39, -34])
                ax.set_axis_off()
                fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)
                fig.tight_layout(pad=0)

                print "Start Save for", graph_type
                print graph_filename
                self.SaveFigureAsImage(graph_filename, fig=fig)
                print "End Save"

    def create_all_overlays(self):

        give_me_full_obs()

        root_folder = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\"
        date_path = arrow_now().format('YYYY-MM-DD')

        config_filename = root_folder + date_path + "\Observations\\" + "range.cfg"

        dir_list = listdir(root_folder+ date_path + "\Observations")

        csv_list = []
        for fn in dir_list:
            if fn[-3:] == "csv":
                csv_list.append(fn)

        len_loc = len(csv_list)
        for fn in csv_list:

            with open(root_folder + date_path + "\Observations\\" + fn, 'r') as f:
                i=0
                for line in f:
                    i+=1
                    line_list = line.split(',')
                    len_details = len(line_list)
                    len_time = i

        len_details+=1

        all_obs = [[["" for k in xrange(len_details)] for j in xrange(len_time)] for i in xrange(len_loc)]

        for i in range(0,len(csv_list)):
            fn = csv_list[i]
            with open(root_folder + date_path + "\Observations\\" + fn, 'r') as f:
                j = 0
                last_time = 0
                for line in f:
                    line_list = line.split(',')
                    this_time = int(line_list[0])
                    if j==0:
                        for k in range(0,len(line_list)):
                            all_obs[i][j][k]=line_list[k]
                        all_obs[i][j][-1] = str(fn).split('.')[0]
                        last_time = this_time
                    elif this_time - last_time != 1800:
                        continue
                    else:
                        for k in range(0, len(line_list)):
                            all_obs[i][j][k] = line_list[k]
                        all_obs[i][j][-1] = str(fn).split('.')[0]
                        last_time = this_time

                    j += 1

        all_obs_sorted = [[["" for k in xrange(len_loc)] for j in xrange(len_time)] for i in xrange(len_details)]

        for i in range(0,len_loc):
            for j in range(0,len_time):
                for k in range(0,len_details):
                    all_obs_sorted[k][j][i] = all_obs[i][j][k]

        for gt in range(1, 6):

            if gt == 1:
                graph_type = "temp"
                min_graph = 0
                max_graph = 40
            elif gt == 2:
                graph_type = "dew"
                min_graph = 0
                max_graph = 25
            elif gt == 3:
                graph_type = "rain"
                min_graph = 0
                max_graph = 80
            elif gt == 4:
                graph_type = "pressure"
                min_graph = 990
                max_graph = 1050
            elif gt == 5:
                graph_type = "lcl"
                min_graph = 0
                max_graph = 3000
            elif gt == 6:
                graph_type = "rel_hum"
                min_graph = 0
                max_graph = 100
            elif gt == 7:
                graph_type = "wind_vel"
                min_graph = 0
                max_graph = 120

            w = 15
            h = 12.5
            fig = plt.figure(figsize=(w, h), facecolor='w', frameon=False, edgecolor="Yellow")

            for i in range(0, len(all_obs_sorted[9])):
                x = []
                y = []
                z = []

                for obs in self.obs_list:
                    for j in range(0, len(all_obs_sorted[9][i])):
                        if obs.code == all_obs_sorted[9][i][j]:
                            try:
                                z.append(float(all_obs_sorted[gt][i][j]))
                                x.append(float(obs.lon))
                                y.append(float(obs.lat))
                            except ValueError:
                                continue
                            break


                if True:
                    try:
                        time_now = arrow_get(all_obs_sorted[0][i][36]).to('Australia/Melbourne').format('HH-mm')
                    except parser.ParserError:
                        continue
                    graph_filename = root_folder + date_path + "\Observations\\" + "vic-" + graph_type + "-" + time_now + ".png"

                    try:
                        with open(graph_filename, 'r'):
                            print "Graph already exists:"
                            print graph_filename
                            continue
                    except IOError:
                        pass

                    resolution = 100
                    xi = linspace(141, 150, resolution)
                    yi = linspace(-39, -34, resolution)
                    zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='cubic')
                    fig.clf()
                    ax = fig.add_subplot(111)
                    ax.contourf(xi, yi, zi, 120, cmap=plt.cm.jet, vmin=min_graph, vmax=max_graph)
                    try:
                        C = ax.contour(xi, yi, zi, 20, linewidths=0.5, colors='k')
                        ax.clabel(C, inline=1, fontsize=6, fmt='%1.0f')
                    except ValueError:
                        pass
                    ax.scatter(x, y, marker='o', c='b', s=.1)
                    ax.axis([141, 150, -39, -34])
                    ax.set_axis_off()
                    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)
                    fig.tight_layout(pad=0)


                    print "Start Save for", graph_type, time_now
                    print graph_filename
                    self.SaveFigureAsImage(graph_filename, fig=fig)
                    print "End Save"

    def create_obs_kml(self):
        create_vic_obs_points(self.obs_list)

    def create_overlays_kml(self):
        create_vic_overlays()

p_obs = ProcessObs()

p_obs.create_all_overlays()

p_obs.create_current_obs_graphs()

p_obs.create_current_overlays()
p_obs.create_overlays_kml()

p_obs.create_obs_kml()

finish_time = arrow_now().timestamp

total_time = finish_time - first_time

print "Process took", total_time, "seconds to complete"
print "Process took", total_time / 60, "minutes to complete"


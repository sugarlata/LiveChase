import arrow
import Download_Observations
from Download_Observations import ObservationLocation
import datetime
import matplotlib.pyplot as plt


class Process_Obs:

    obs_list = []
    loc_names = []

    def __init__(self):

        self.obs_list, self.loc_names = Download_Observations.give_me_vic_obs()

    def update_observations(self):

        self.obs_list, self.loc_names = Download_Observations.give_me_vic_obs()

    def create_graph(self, data):

        pass

    def create_obs_graphs(self):

        location_objects = []

        for i in range(0, len(self.loc_names)):

            root_folder = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\"
            date_path = arrow.now().format('YYYY-MM-DD')

            for j in range(0, len(self.obs_list)):
                if self.loc_names[i] == self.obs_list[j].code:

                    code = self.obs_list[j].code
                    loc_name =  self.obs_list[j].loc_name
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
        for k in self.loc_names:

            loc_obs_temp = []
            loc_obs_dew = []
            loc_obs_rain = []
            loc_obs_pressure = []
            loc_obs_lcl = []
            loc_obs_rel_hum = []
            loc_obs_wind_vel = []
            loc_obs_wind_dir = []

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

            if k == "tatura":
                if len(loc_obs_temp)>1:

                    # Code to create graph goes here.

                    x = []
                    y = []
                    for m in loc_obs_temp:
                        x.append(datetime.datetime.fromtimestamp(float(m[0])))
                        y.append(m[1])

                    plt.plot(x,y)

                    plt.gcf().autofmt_xdate()

                    plt.show()

p_obs = Process_Obs()



p_obs.create_obs_graphs()


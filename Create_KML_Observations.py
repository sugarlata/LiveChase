from arrow import now as arrow_now
from arrow import get as arrow_get
from os import listdir
import simplekml


def create_vic_overlays():

    root_folder = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\"
    date_path = arrow_now().format('YYYY-MM-DD')

    vic_temp_list = []
    vic_dew_list = []
    vic_rain_list = []
    vic_pressure_list = []
    vic_rel_hum_list = []
    vic_lcl_list = []
    vic_wind_vel_list = []
    for fn in listdir(root_folder + date_path + "\Observations"):
        if fn[:3] == "vic":
            if fn[4:8] == "temp":
                print fn
                vic_temp_list.append(fn)
            if fn[4:8] == "dew-":
                vic_dew_list.append(fn)
            if fn[4:8] == "rain":
                vic_rain_list.append(fn)
            if fn[4:8] == "pres":
                vic_pressure_list.append(fn)
            if fn[4:8] == "rel_":
                vic_rel_hum_list.append(fn)
            if fn[4:8] == "lcl-":
                vic_lcl_list.append(fn)
            if fn[4:8] == "wind":
                vic_wind_vel_list.append(fn)

    vic_temp_list.sort()
    vic_dew_list.sort()
    vic_pressure_list.sort()
    vic_rain_list.sort()
    vic_lcl_list.sort()
    vic_rel_hum_list.sort()
    vic_wind_vel_list.sort()

    # Temperature Graphs

    kml = simplekml.Kml()
    kml_temp_folder = kml.newfolder(name='Victorian Temperature Overlays')
    temp_overlays = []

    for i in range(0, len(vic_temp_list)):
        ov_name = "Temperature"
        ov_time = arrow_get(vic_temp_list[i].split('.')[0][-5:],'HH-mm').format('HH:mm')
        ov_start = arrow_get(date_path + " " + str(ov_time), 'YYYY-MM-DD HH:mm', tzinfo='Australia/Melbourne')
        ov_end = arrow_get(ov_start.timestamp + 60*30).to('Australia/Melbourne')
        temp_overlays.insert(i,kml_temp_folder.newgroundoverlay(name=str(ov_name) + " " + ov_time))
        temp_overlays[i].icon.href = root_folder + date_path + "\Observations\\" + vic_temp_list[i]
        temp_overlays[i].latlonbox.north = -34
        temp_overlays[i].latlonbox.south = -39
        temp_overlays[i].latlonbox.east = 150
        temp_overlays[i].latlonbox.west = 141
        temp_overlays[i].timespan.begin = ov_start
        temp_overlays[i].timespan.end = ov_end
        temp_overlays[i].color = "65ffffff"

        if i > 0:
            temp_overlays[i-1].visibility = 0

    # Dew Point Graphs

    kml_dew_folder = kml.newfolder(name='Victorian Dew Point Overlays')
    dew_overlays = []

    for i in range(0, len(vic_dew_list)):
        ov_name = "Dew Point"
        ov_time = arrow_get(vic_dew_list[i].split('.')[0][-5:], 'HH-mm').format('HH:mm')
        ov_start = arrow_get(date_path + " " + str(ov_time), 'YYYY-MM-DD HH:mm', tzinfo='Australia/Melbourne')
        ov_end = arrow_get(ov_start.timestamp + 60 * 30).to('Australia/Melbourne')
        dew_overlays.insert(i, kml_dew_folder.newgroundoverlay(name=str(ov_name) + " " + ov_time))
        dew_overlays[i].icon.href = root_folder + date_path + "\Observations\\" + vic_dew_list[i]
        dew_overlays[i].latlonbox.north = -34
        dew_overlays[i].latlonbox.south = -39
        dew_overlays[i].latlonbox.east = 150
        dew_overlays[i].latlonbox.west = 141
        dew_overlays[i].timespan.begin = ov_start
        dew_overlays[i].timespan.end = ov_end
        dew_overlays[i].color = "65ffffff"

        if i > 0:
            dew_overlays[i - 1].visibility = 0

    # Rain Graphs

    kml_rain_folder = kml.newfolder(name='Victorian Rain Overlays')
    rain_overlays = []

    for i in range(0, len(vic_rain_list)):
        ov_name = "Rain"
        ov_time = arrow_get(vic_rain_list[i].split('.')[0][-5:], 'HH-mm').format('HH:mm')
        ov_start = arrow_get(date_path + " " + str(ov_time), 'YYYY-MM-DD HH:mm', tzinfo='Australia/Melbourne')
        ov_end = arrow_get(ov_start.timestamp + 60 * 30).to('Australia/Melbourne')
        rain_overlays.insert(i, kml_rain_folder.newgroundoverlay(name=str(ov_name) + " " + ov_time))
        rain_overlays[i].icon.href = root_folder + date_path + "\Observations\\" + vic_rain_list[i]
        rain_overlays[i].latlonbox.north = -34
        rain_overlays[i].latlonbox.south = -39
        rain_overlays[i].latlonbox.east = 150
        rain_overlays[i].latlonbox.west = 141
        rain_overlays[i].timespan.begin = ov_start
        rain_overlays[i].timespan.end = ov_end
        rain_overlays[i].color = "65ffffff"

        if i > 0:
            rain_overlays[i - 1].visibility = 0

    # Pressure Graphs

    kml_pressure_folder = kml.newfolder(name='Victorian Pressure Overlays')
    pressure_overlays = []

    for i in range(0, len(vic_pressure_list)):
        ov_name = "Pressure"
        ov_time = arrow_get(vic_pressure_list[i].split('.')[0][-5:], 'HH-mm').format('HH:mm')
        ov_start = arrow_get(date_path + " " + str(ov_time), 'YYYY-MM-DD HH:mm', tzinfo='Australia/Melbourne')
        ov_end = arrow_get(ov_start.timestamp + 60 * 30).to('Australia/Melbourne')
        pressure_overlays.insert(i, kml_pressure_folder.newgroundoverlay(name=str(ov_name) + " " + ov_time))
        pressure_overlays[i].icon.href = root_folder + date_path + "\Observations\\" + vic_pressure_list[i]
        pressure_overlays[i].latlonbox.north = -34
        pressure_overlays[i].latlonbox.south = -39
        pressure_overlays[i].latlonbox.east = 150
        pressure_overlays[i].latlonbox.west = 141
        pressure_overlays[i].timespan.begin = ov_start
        pressure_overlays[i].timespan.end = ov_end
        pressure_overlays[i].color = "65ffffff"

        if i > 0:
            pressure_overlays[i - 1].visibility = 0

    # Relative Humidity Graphs

    kml_rel_hum_folder = kml.newfolder(name='Victorian Relative Humidity Overlays')
    rel_hum_overlays = []

    for i in range(0, len(vic_rel_hum_list)):
        ov_name = "Relative Humidity"
        ov_time = arrow_get(vic_rel_hum_list[i].split('.')[0][-5:], 'HH-mm').format('HH:mm')
        ov_start = arrow_get(date_path + " " + str(ov_time), 'YYYY-MM-DD HH:mm', tzinfo='Australia/Melbourne')
        ov_end = arrow_get(ov_start.timestamp + 60 * 30).to('Australia/Melbourne')
        rel_hum_overlays.insert(i, kml_rel_hum_folder.newgroundoverlay(name=str(ov_name) + " " + ov_time))
        rel_hum_overlays[i].icon.href = root_folder + date_path + "\Observations\\" + vic_rel_hum_list[i]
        rel_hum_overlays[i].latlonbox.north = -34
        rel_hum_overlays[i].latlonbox.south = -39
        rel_hum_overlays[i].latlonbox.east = 150
        rel_hum_overlays[i].latlonbox.west = 141
        rel_hum_overlays[i].timespan.begin = ov_start
        rel_hum_overlays[i].timespan.end = ov_end
        rel_hum_overlays[i].color = "65ffffff"

        if i > 0:
            rel_hum_overlays[i - 1].visibility = 0

    # Lifted Condensation Level Graphs

    kml_lcl_folder = kml.newfolder(name='Victorian Lifted Condensation Level Overlays')
    lcl_overlays = []

    for i in range(0, len(vic_lcl_list)):
        ov_name = "Lifted Condensation Level"
        ov_time = arrow_get(vic_lcl_list[i].split('.')[0][-5:], 'HH-mm').format('HH:mm')
        ov_start = arrow_get(date_path + " " + str(ov_time), 'YYYY-MM-DD HH:mm', tzinfo='Australia/Melbourne')
        ov_end = arrow_get(ov_start.timestamp + 60 * 30).to('Australia/Melbourne')
        lcl_overlays.insert(i, kml_lcl_folder.newgroundoverlay(name=str(ov_name) + " " + ov_time))
        lcl_overlays[i].icon.href = root_folder + date_path + "\Observations\\" + vic_lcl_list[i]
        lcl_overlays[i].latlonbox.north = -34
        lcl_overlays[i].latlonbox.south = -39
        lcl_overlays[i].latlonbox.east = 150
        lcl_overlays[i].latlonbox.west = 141
        lcl_overlays[i].timespan.begin = ov_start
        lcl_overlays[i].timespan.end = ov_end
        lcl_overlays[i].color = "65ffffff"

        if i > 0:
            lcl_overlays[i - 1].visibility = 0

    # Wind Speed Graphs

    kml_wind_vel_folder = kml.newfolder(name='Victorian Wind Speed Overlays')
    wind_vel_overlays = []

    for i in range(0, len(vic_wind_vel_list)):
        ov_name = "Wind Speed"
        ov_time = arrow_get(vic_wind_vel_list[i].split('.')[0][-5:], 'HH-mm').format('HH:mm')
        ov_start = arrow_get(date_path + " " + str(ov_time), 'YYYY-MM-DD HH:mm', tzinfo='Australia/Melbourne')
        ov_end = arrow_get(ov_start.timestamp + 60 * 30).to('Australia/Melbourne')
        wind_vel_overlays.insert(i, kml_wind_vel_folder.newgroundoverlay(name=str(ov_name) + " " + ov_time))
        wind_vel_overlays[i].icon.href = root_folder + date_path + "\Observations\\" + vic_wind_vel_list[i]
        wind_vel_overlays[i].latlonbox.north = -34
        wind_vel_overlays[i].latlonbox.south = -39
        wind_vel_overlays[i].latlonbox.east = 150
        wind_vel_overlays[i].latlonbox.west = 141
        wind_vel_overlays[i].timespan.begin = ov_start
        wind_vel_overlays[i].timespan.end = ov_end
        wind_vel_overlays[i].color = "65ffffff"

        if i > 0:
            wind_vel_overlays[i - 1].visibility = 0

    kml.save(root_folder + date_path + "\Vic Overlay.kml")

def create_vic_obs_points(obs_list):
    pass

    root_folder = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\"
    date_path = arrow_now().format('YYYY-MM-DD')

    # Need to create a point for each location in Victoria,
    # Each point will be placed on the location (need to refine the GPS according to station location
    # Each Station to have the current observations in the balloon (not time coded)
    # Each station to have the graphs in the pictures also

    kml = simplekml.Kml()
    kml_obs_folder = kml.newfolder(name='Victorian Observation Locations')
    location_list = []

    description_block = r"""<![CDATA[<font size = "6">
<h1>$NAME</h1>
<h2>Observations:</h2>
<table width="277">
<tbody>
<tr>
<td><font size = "6">Time</td></font>
<td><font size = "6">$TIME</td></font>
</tr>
<tr>
<td><font size = "6">Temperature</td></font>
<td><font size = "6">$TEMP</td></font>
</tr>
<tr>
<td><font size = "6">Dew Point</td></font>
<td><font size = "6">$DEW</td></font>
</tr>
<tr>
<td><font size = "6">Rain since 9am</td></font>
<td><font size = "6">$RAIN</td></font>
</tr>
<tr>
<td><font size = "6">Pressure</td></font>
<td><font size = "6">$PRESSURE</td></font>
</tr>
<tr>
<td><font size = "6">Relative Humidity</td></font>
<td><font size = "6">$REL_HUM</td></font>
</tr>
<tr>
<td><font size = "6">LCL</td></font>
<td><font size = "6">$LCL</td></font>
</tr>
<tr>
<td><font size = "6">Wind Speed</td></font>
<td><font size = "6">$WIND_VEL</td></font>
</tr>
<tr>
<td><font size = "6">Wind Direction</td></font>
<td><font size = "6">$WIND_DIR</td></font>
</tr>
</tbody>
</table>
<h2>Graphs</h2>
<h3>Temperature</h3>
<p>$GR_TEMP</p>
<h3>Dew Points</h3>
<p>$GR_DEW</p>
<h3>Rain since 9am</h3>
<p>$GR_RAIN</p>
<h3>Pressure</h3>
<p>$GR_PRESSURE</p>
<h3>Relative Humidity</h3>
<p>$GR_REL_HUM</p>
<h3>Lifted Condesation Level</h3>
<p>$GR_LCL</p>
<h3>Wind Speed</h3>
<p>$GR_WIND_VEL</p>
</font>]]>"""

    for i in range(0,len(obs_list)):
        code = obs_list[i].code
        lat = obs_list[i].lat
        lon = obs_list[i].lon
        station_name = obs_list[i].loc_name
        temp = obs_list[i].temp
        dew = obs_list[i].dew
        rain = obs_list[i].rain
        pressure = obs_list[i].pressure
        rel_hum = obs_list[i].rel_hum
        lcl = obs_list[i].lcl
        wind_vel = obs_list[i].wind_vel

        location_list.insert(i, kml_obs_folder.newpoint(name=station_name))
        location_list[i].coords = [(lon, lat)]
        location_list[i].style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/ylw-blank.png'

        loc_desc = description_block
        loc_desc = loc_desc.replace('$NAME', obs_list[i].loc_name)
        loc_desc = loc_desc.replace('$TIME', obs_list[i].time)
        loc_desc = loc_desc.replace('$TEMP', obs_list[i].temp)
        loc_desc = loc_desc.replace('$DEW', obs_list[i].dew)
        loc_desc = loc_desc.replace('$RAIN', obs_list[i].rain)
        loc_desc = loc_desc.replace('$PRESSURE', obs_list[i].pressure)
        loc_desc = loc_desc.replace('$REL_HUM', obs_list[i].rel_hum)
        loc_desc = loc_desc.replace('$LCL', str(obs_list[i].lcl))
        loc_desc = loc_desc.replace('$WIND_VEL', obs_list[i].wind_vel)
        loc_desc = loc_desc.replace('$WIND_DIR', obs_list[i].wind_dir)
        
        dir_cont = listdir(root_folder + date_path + "\Observations")
        time_now = arrow_now().to('Australia/Melbourne').format('YYYY-MM-DD') + ' ' + obs_list[i].time
        time_fn = arrow_get(time_now, 'YYYY-MM-DD HH:mm', tzinfo="Australia/Melbourne").to('Australia/Melbourne').format('HH-mm')

        gr_temp = root_folder + date_path + "\Observations\\" + obs_list[i].code + '-temperature-' + time_fn + '.png'
        try:
            with open(gr_temp, 'r'):
                gr_temp = "file:///" + gr_temp.replace("\\", "/").replace(" ", "%20").lower()
                loc_desc = loc_desc.replace('$GR_TEMP', '<img src="' + gr_temp + '" width ="1000">')
        except IOError:
            gr_temp = "file:///" + gr_temp.replace("\\", "/").replace(" ", "%20").lower()
            loc_desc = loc_desc.replace('$GR_TEMP', '<img src="' + gr_temp + '" width ="1000"></p>\n<p>Graph Doesn\'t exist')


        gr_dew = root_folder + date_path + "\Observations\\" + obs_list[i].code + '-dew-point-' + time_fn + '.png'
        try:
            with open(gr_dew, 'r'):
                gr_dew = "file:///" + gr_dew.replace("\\", "/").replace(" ", "%20").lower()
                loc_desc = loc_desc.replace('$GR_DEW', '<img src="' + gr_dew + '"/>')
        except IOError:
            gr_dew = "file:///" + gr_dew.replace("\\", "/").replace(" ", "%20").lower()
            loc_desc = loc_desc.replace('$GR_DEW', '<img src="' + gr_dew + '" width ="1000"></p>\n<p>Graph Doesn\'t exist')


        gr_rain = root_folder + date_path + "\Observations\\" + obs_list[i].code + '-rain-' + time_fn + '.png'
        try:
            with open(gr_rain, 'r'):
                gr_rain = "file:///" + gr_rain.replace("\\", "/").replace(" ", "%20").lower()
                loc_desc = loc_desc.replace('$GR_RAIN', '<img src="' + gr_rain + '"/>')
        except IOError:
            gr_rain = "file:///" + gr_rain.replace("\\", "/").replace(" ", "%20").lower()
            loc_desc = loc_desc.replace('$GR_RAIN', '<img src="' + gr_rain + '" width ="1000"></p>\n<p>Graph Doesn\'t exist')


        gr_pressure = root_folder + date_path + "\Observations\\" + obs_list[i].code + '-pressure-' + time_fn + '.png'
        try:
            with open(gr_pressure, 'r'):
                gr_pressure = "file:///" + gr_pressure.replace("\\", "/").replace(" ", "%20").lower()
                loc_desc = loc_desc.replace('$GR_PRESSURE', '<img src="' + gr_pressure + '"/>')
        except IOError:
            gr_pressure = "file:///" + gr_pressure.replace("\\", "/").replace(" ", "%20").lower()
            loc_desc = loc_desc.replace('$GR_PRESSURE', '<img src="' + gr_pressure + '" width ="1000"></p>\n<p>Graph Doesn\'t exist')


        gr_rel_hum = root_folder + date_path + "\Observations\\" + obs_list[i].code + '-rel_hum-' + time_fn + '.png'
        try:
            with open(gr_rel_hum, 'r'):
                gr_rel_hum = "file:///" + gr_rel_hum.replace("\\", "/").replace(" ", "%20").lower()
                loc_desc = loc_desc.replace('$GR_REL_HUM', '<img src="' + gr_rel_hum + '"/>')
        except IOError:
            gr_rel_hum = "file:///" + gr_rel_hum.replace("\\", "/").replace(" ", "%20").lower()
            loc_desc = loc_desc.replace('$GR_REL_HUM', '<img src="' + gr_rel_hum + '" width ="1000"></p>\n<p>Graph Doesn\'t exist')


        gr_lcl = root_folder + date_path + "\Observations\\" + obs_list[i].code + '-lcl-' + time_fn + '.png'
        try:
            with open(gr_lcl, 'r'):
                gr_lcl = "file:///" + gr_lcl.replace("\\", "/").replace(" ", "%20").lower()
                loc_desc = loc_desc.replace('$GR_LCL', '<img src="' + gr_lcl + '"/>')
        except IOError:
            gr_lcl = "file:///" + gr_lcl.replace("\\", "/").replace(" ", "%20").lower()
            loc_desc = loc_desc.replace('$GR_LCL', '<img src="' + gr_lcl + '" width ="1000"></p>\n<p>Graph Doesn\'t exist')


        gr_wind_vel = root_folder + date_path + "\Observations\\" + obs_list[i].code + '-wind-' + time_fn + '.png'
        try:
            with open(gr_wind_vel, 'r'):
                gr_wind_vel = "file:///" + gr_wind_vel.replace("\\", "/").replace(" ", "%20").lower()
                loc_desc = loc_desc.replace('$GR_WIND_VEL', '<img src="' + gr_wind_vel + '"/>')
        except IOError:
            gr_wind_vel = "file:///" + gr_wind_vel.replace("\\", "/").replace(" ", "%20").lower()
            loc_desc = loc_desc.replace('$GR_WIND_VEL', '<img src="' + gr_wind_vel + '" width ="1000"></p>\n<p>Graph Doesn\'t exist')












        location_list[i].description = loc_desc

    kml.save('C:\\Users\\Nathan\\Documents\\Storm Chasing\\temph.kml')
    print "kml created"

from StringIO import StringIO
from urllib import urlopen
from arrow import get as arrow_get
from arrow import now as arrow_now
from time import sleep
from os import chdir
from os import mkdir
import csv


class ObservationLocation:

    code = ""
    loc_name = ""
    lat = float()
    lon = float()
    height = float()

    time = ""
    temp = float()
    dew = float()
    rain = float()
    pressure = float()
    lcl = float()
    rel_hum = ""
    wind_vel = float()
    wind_dir = ""

    def __init__(self, code, loc_name, lat, lon, height):

        self.code = code
        self.loc_name = loc_name
        self.lat = lat
        self.lon = lon
        self.height = height


def give_me_vic_obs():

    string_of_observation_locations = """aireys-inlet,Aireys Inlet,-38.4583,144.0883,105
avalon,Avalon Airport,-38.0287,144.4783,10.6
bairnsdale,Bairnsdale Airport,-37.8817,147.5669,49.4
ballarat,Ballarat Aerodrome,-37.5127,143.7911,435.2
bendigo,Bendigo Airport,-36.7395,144.3266,208
geelong-racecourse,Breakwater (Geelong Racecourse),-38.1737,144.3765,12.9
cape-nelson,Cape Nelson Lighthouse,-38.4306,141.5437,45.4
cape-otway,Cape Otway Lighthouse,-38.8556,143.5128,82
casterton,Casterton,-37.583,141.3339,130.6
cerberus,Cerberus,-38.3646,145.1785,12.69
charlton,Charlton,-36.2847,143.3341,131.7
mount-gellibrand,Colac (Mount Gellibrand),-38.2333,143.7925,261
coldstream,Coldstream,-37.7239,145.4092,83
combienbar,Combienbar AWS,-37.3417,149.0228,640
yanakie,Corner Inlet (Yanakie),-38.8051,146.1939,13.3
dartmoor,Dartmoor,-37.9222,141.2614,51
mount-hotham-airport,Dinner Plain (Mount Hotham Airport),-37.0491,147.3347,1295.4
east-sale,East Sale Airport,-38.1156,147.1322,4.6
edenhope,Edenhope Airport,-37.0222,141.2657,155
eildon-fire-tower,Eildon Fire Tower,-37.2091,145.8423,637
essendon-airport,Essendon Airport,-37.7276,144.9066,78.4
falls-creek,Falls Creek,-36.8708,147.2755,1765
ferny-creek,Ferny Creek,-37.8748,145.3496,512.9
frankston,Frankston AWS,-38.1481,145.1156,6
gabo-island,Gabo Island Lighthouse,-37.5679,149.9158,15.2
gelantipy,Gelantipy,-37.22,148.2625,755
mount-william,Grampians (Mount William),-37.295,142.6039,1150
hamilton,Hamilton Airport,-37.6486,142.0636,241.1
hopetoun-airport,Hopetoun Airport,-35.7151,142.3569,77.3
hunters-hill,Hunters Hill,-36.2136,147.5394,981
kanagulk,Kanagulk,-37.1169,141.8031,188.8
warracknabeal-airport,Kellalac (Warracknabeal Airport),-36.3204,142.4161,118.3
kyabram,Kyabram,-36.335,145.0638,105
laverton,Laverton RAAF,-37.8565,144.7566,20.1
longerenong,Longerenong,-36.6722,142.2991,133
mallacoota,Mallacoota,-37.5976,149.7289,22
mangalore,Mangalore Airport,-36.8886,145.1859,140.8
melbourne-olympic-park,Melbourne (Olympic Park),-37.8255,144.9816,7.53
melbourne-airport,Melbourne Airport,-37.6655,144.8321,113.4
mildura,Mildura Airport,-34.2358,142.0867,50
moorabbin-airport,Moorabbin Airport,-37.98,145.0962,12.1
mortlake,Mortlake Racecourse,-38.0737,142.7744,130
latrobe-valley,Morwell (Latrobe Valley Airport),-38.2094,146.4747,55.7
mount-baw-baw,Mount Baw Baw,-37.8383,146.2747,1561
mount-buller,Mount Buller,-37.145,146.4394,1707
mount-moornapa,Mount Moornapa,-37.7481,147.1428,480
mount-nowa-nowa,Mount Nowa Nowa,-37.6924,148.0908,350
nhill-aerodrome,Nhill Aerodrome,-36.3092,141.6486,138.9
omeo,Omeo,-37.1017,147.6008,689.8
orbost,Orbost,-37.6922,148.4667,62.65
port-fairy,Port Fairy AWS,-38.3906,142.2347,10
portland-airport,Portland (Cashmore Airport),-38.3148,141.4705,80.9
portland-harbour,Portland NTC AWS,-38.3439,141.6136,0
pound-creek,Pound Creek,-38.6297,145.8107,3
redesdale,Redesdale,-37.0194,144.5203,290
rhyll,Rhyll,-38.4612,145.3101,13.4
rutherglen,Rutherglen Research,-36.1047,146.5094,175
scoresby,Scoresby Research Institute,-37.871,145.2561,80
sheoaks,Sheoaks,-37.9075,144.1303,236.7
shepparton,Shepparton Airport,-36.4289,145.3947,113.9
stawell,Stawell Aerodrome,-37.072,142.7402,235.36
swan-hill,Swan Hill Aerodrome,-35.3766,143.5416,71
tatura,Tatura Inst Sustainable Ag,-36.4378,145.2672,114
viewbank,Viewbank,-37.7408,145.0972,66.1
kilmore-gap,Wallan (Kilmore Gap),-37.3807,144.9654,527.8
walpeup,Walpeup Research,-35.1201,142.004,105
wangaratta,Wangaratta Aero,-36.4206,146.3056,152.6
warrnambool,Warrnambool Airport NDB,-38.2867,142.4522,70.8
westmere,Westmere,-37.7067,142.9378,226
wilsons-promontory,Wilsons Promontory Lighthouse,-39.1297,146.4244,95
yarram-airport,Yarram Airport,-38.5647,146.7479,17.9
yarrawonga,Yarrawonga,-36.0294,146.0306,128.9"""

    print "Beginning URL Load"
    buf = StringIO(string_of_observation_locations)

    loc_names = []
    obs_list = []

    for i in buf:
        loc=str(i).replace('\n','').split(',')
        obs_list.append(ObservationLocation(loc[0].lstrip(),loc[1],float(loc[2]),float(loc[3]),float(loc[4])))
        loc_names.append(loc[0].lstrip())

    urladdy = "http://www.bom.gov.au/vic/observations/vicall.shtml"

    print "Opening URL"
    reader = urlopen(urladdy)

    full_page = StringIO(str(reader.read()))

    print "Scraping URL"
    for i in full_page:
        line = str(i).replace('\n','')

        for j in range(0,len(obs_list)):

            if obs_list[j].code in line:

                if '-datetime ' in line:
                    obs_list[j].time = line.split('>')[1].split('<')[0].split('/')[1]

                if '-tmp ' in line:
                    obs_list[j].temp = line.split('>')[1].split('<')[0]

                if '-dewpoint ' in line:
                    obs_list[j].dew = line.split('>')[1].split('<')[0]

                if '-rainsince9am ' in line:
                    obs_list[j].rain = line.split('>')[1].split('<')[0]

                if '-press ' in line:
                    obs_list[j].pressure =  line.split('>')[1].split('<')[0]

                if '-relhum ' in line:
                    obs_list[j].rel_hum = line.split('>')[1].split('<')[0]

                if '-wind-spd-kmh ' in line:
                    obs_list[j].wind_vel = line.split('>')[1].split('<')[0]

                if '-wind-dir ' in line:
                    obs_list[j].wind_dir = line.split('>')[1].split('<')[0]

    for i in range(0,len(obs_list)):

        temp_ = obs_list[i].temp
        dp_ = obs_list[i].dew

        if temp_ == "-" or dp_ == "-":
            obs_list[i].lcl = "-"
            continue

        lcl = 125*(float(temp_)-float(dp_))

        obs_list[i].lcl = lcl+obs_list[i].height

    print "Saving CSV Files"
    
    temp=[]
    dew=[]
    rain=[]
    pressure=[]
    rel_hum=[]
    lcl=[]
    wind_vel=[]
    
    
    for j in range(0, len(obs_list)):

        root_folder = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\"
        date_path = arrow_now().format('YYYY-MM-DD')
        
        try:
            chdir(root_folder + date_path)
        except WindowsError:
            mkdir(root_folder + date_path)

        try:
            chdir(root_folder + date_path + "\Observations")
        except WindowsError:
            mkdir(root_folder + date_path + "\Observations")

        try:
            temp.append(float(obs_list[j].temp))
        except ValueError:
            pass

        try:
            dew.append(float(obs_list[j].dew))
        except ValueError:
            pass

        try:
            rain.append(float(obs_list[j].rain))
        except ValueError:
            pass

        try:
            pressure.append(float(obs_list[j].pressure))
        except ValueError:
            pass

        try:
            rel_hum.append(float(obs_list[j].rel_hum))
        except ValueError:
            pass

        try:
            lcl.append(float(obs_list[j].lcl))
        except ValueError:
            pass

        try:
            wind_vel.append(float(obs_list[j].wind_vel))
        except ValueError:
            pass

        last_line = ""
        csv_filename = root_folder + date_path + "\Observations\\" + obs_list[j].code + ".csv"

        print obs_list[j].time

        local_time = str(arrow_now().format('YYYY-MM-DD')) + " " + str(arrow_get(obs_list[j].time, 'HH:mmA').format('HH:mm'))
        ts = arrow_get(local_time, 'YYYY-MM-DD HH:mm', tzinfo='Australia/Melbourne').timestamp

        write_line = str(ts) + "," + str(obs_list[j].temp) + "," + str(obs_list[j].dew) + "," + str(obs_list[j].rain) + "," + str(obs_list[j].pressure) + "," + str(obs_list[j].lcl) + "," + str(obs_list[j].rel_hum) + "," + str(obs_list[j].wind_vel) + "," + str(obs_list[j].wind_dir) + "\n"

        try:
            with open(csv_filename, 'r') as f:
                for line in f:
                    last_line = line

            if write_line == last_line:
                pass
            else:
                with open(csv_filename, 'a') as g:
                    g.write(write_line)

        except IOError:
            with open(csv_filename, 'a') as g:
                g.write(write_line)

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

    try:
        with open(config_filename, 'r') as f:
            # Determine min / max temp
            line = f.readline()
            line_vals = line.split(',')
            try:
                if min(temp) < float(line_vals[0]):
                    min_temp = min(temp)
                else:
                    min_temp = float(line_vals[0])
                if max(temp) > float(line_vals[1]):
                    max_temp = max(temp)
                else:
                    max_temp = float(line_vals[1])
            except ValueError:
                pass

            # Determine min / max dew
            line = f.readline()
            line_vals = line.split(',')
            try:
                if min(dew) < float(line_vals[0]):
                    min_dew = min(dew)
                else:
                    min_dew = float(line_vals[0])
                if max(dew) > float(line_vals[1]):
                    max_dew = max(dew)
                else:
                    max_dew = float(line_vals[1])
            except ValueError:
                pass
        
            # Determine min / max rain
            line = f.readline()
            line_vals = line.split(',')
            try:
                if min(rain) < float(line_vals[0]):
                    min_rain = min(rain)
                else:
                    min_rain = float(line_vals[0])
                if max(rain) > float(line_vals[1]):
                    max_rain = max(rain)
                else:
                    max_rain = float(line_vals[1])
            except ValueError:
                pass

            # Determine min / max pressure
            line = f.readline()
            line_vals = line.split(',')
            try:
                if min(pressure) < float(line_vals[0]):
                    min_pressure = min(pressure)
                else:
                    min_pressure = float(line_vals[0])
                if max(pressure) > float(line_vals[1]):
                    max_pressure = max(pressure)
                else:
                    max_pressure = float(line_vals[1])
            except ValueError:
                pass
            
            # Determine min / max rel_hum
            line = f.readline()
            line_vals = line.split(',')
            try:
                if min(rel_hum) < float(line_vals[0]):
                    min_rel_hum = min(rel_hum)
                else:
                    min_rel_hum = float(line_vals[0])
                if max(rel_hum) > float(line_vals[1]):
                    max_rel_hum = max(rel_hum)
                else:
                    max_rel_hum = float(line_vals[1])
            except ValueError:
                pass
            
            # Determine min / max lcl
            line = f.readline()
            line_vals = line.split(',')
            try:
                if min(lcl) < float(line_vals[0]):
                    min_lcl = min(lcl)
                else:
                    min_lcl = float(line_vals[0])
                if max(lcl) > float(line_vals[1]):
                    max_lcl = max(lcl)
                else:
                    max_lcl = float(line_vals[1])
            except ValueError:
                pass
            
            # Determine min / max wind_vel
            line = f.readline()
            line_vals = line.split(',')
            try:
                if min(wind_vel) < float(line_vals[0]):
                    min_wind_vel = min(wind_vel)
                else:
                    min_wind_vel = float(line_vals[0])
                if max(wind_vel) > float(line_vals[1]):
                    max_wind_vel = max(wind_vel)
                else:
                    max_wind_vel = float(line_vals[1])
            except ValueError:
                pass
            
    except IOError:
            min_temp = 0
            max_temp = 45
            min_dew = -10
            max_dew = 25
            min_pressure = 995
            max_pressure = 1030
            min_rain = 0
            max_rain = 40
            min_rel_hum = 0
            max_rel_hum = 100
            min_lcl = 0
            max_lcl = 3000
            min_wind_vel = 0
            max_wind_vel = 5
    
    with open(config_filename, 'w') as f:
        line = str(min_temp) + "," + str(max_temp) + "\n"
        f.writelines(line)
        line = str(min_dew) + "," + str(max_dew) + "\n"
        f.writelines(line)
        line = str(min_rain) + "," + str(max_rain) + "\n"
        f.writelines(line)
        line = str(min_pressure) + "," + str(max_pressure) + "\n"
        f.writelines(line)
        line = str(min_rel_hum) + "," + str(max_rel_hum) + "\n"
        f.writelines(line)
        line = str(min_lcl) + "," + str(max_lcl) + "\n"
        f.writelines(line)
        line = str(min_wind_vel) + "," + str(max_wind_vel) + "\n"
        f.writelines(line)

    print "Finished Saving CSV Files"

    return obs_list, loc_names

def give_me_full_obs():
    string_of_observation_locations = """aireys-inlet,Aireys Inlet,-38.4583,144.0883,105
avalon,Avalon Airport,-38.0287,144.4783,10.6
bairnsdale,Bairnsdale Airport,-37.8817,147.5669,49.4
ballarat,Ballarat Aerodrome,-37.5127,143.7911,435.2
bendigo,Bendigo Airport,-36.7395,144.3266,208
geelong-racecourse,Breakwater (Geelong Racecourse),-38.1737,144.3765,12.9
cape-nelson,Cape Nelson Lighthouse,-38.4306,141.5437,45.4
cape-otway,Cape Otway Lighthouse,-38.8556,143.5128,82
casterton,Casterton,-37.583,141.3339,130.6
cerberus,Cerberus,-38.3646,145.1785,12.69
charlton,Charlton,-36.2847,143.3341,131.7
mount-gellibrand,Colac (Mount Gellibrand),-38.2333,143.7925,261
coldstream,Coldstream,-37.7239,145.4092,83
combienbar,Combienbar AWS,-37.3417,149.0228,640
yanakie,Corner Inlet (Yanakie),-38.8051,146.1939,13.3
dartmoor,Dartmoor,-37.9222,141.2614,51
mount-hotham-airport,Dinner Plain (Mount Hotham Airport),-37.0491,147.3347,1295.4
east-sale,East Sale Airport,-38.1156,147.1322,4.6
edenhope,Edenhope Airport,-37.0222,141.2657,155
eildon-fire-tower,Eildon Fire Tower,-37.2091,145.8423,637
essendon-airport,Essendon Airport,-37.7276,144.9066,78.4
falls-creek,Falls Creek,-36.8708,147.2755,1765
ferny-creek,Ferny Creek,-37.8748,145.3496,512.9
frankston,Frankston AWS,-38.1481,145.1156,6
gabo-island,Gabo Island Lighthouse,-37.5679,149.9158,15.2
gelantipy,Gelantipy,-37.22,148.2625,755
mount-william,Grampians (Mount William),-37.295,142.6039,1150
hamilton,Hamilton Airport,-37.6486,142.0636,241.1
hopetoun-airport,Hopetoun Airport,-35.7151,142.3569,77.3
hunters-hill,Hunters Hill,-36.2136,147.5394,981
kanagulk,Kanagulk,-37.1169,141.8031,188.8
warracknabeal-airport,Kellalac (Warracknabeal Airport),-36.3204,142.4161,118.3
kyabram,Kyabram,-36.335,145.0638,105
laverton,Laverton RAAF,-37.8565,144.7566,20.1
longerenong,Longerenong,-36.6722,142.2991,133
mallacoota,Mallacoota,-37.5976,149.7289,22
mangalore,Mangalore Airport,-36.8886,145.1859,140.8
melbourne-olympic-park,Melbourne (Olympic Park),-37.8255,144.9816,7.53
melbourne-airport,Melbourne Airport,-37.6655,144.8321,113.4
mildura,Mildura Airport,-34.2358,142.0867,50
moorabbin-airport,Moorabbin Airport,-37.98,145.0962,12.1
mortlake,Mortlake Racecourse,-38.0737,142.7744,130
latrobe-valley,Morwell (Latrobe Valley Airport),-38.2094,146.4747,55.7
mount-baw-baw,Mount Baw Baw,-37.8383,146.2747,1561
mount-buller,Mount Buller,-37.145,146.4394,1707
mount-moornapa,Mount Moornapa,-37.7481,147.1428,480
mount-nowa-nowa,Mount Nowa Nowa,-37.6924,148.0908,350
nhill-aerodrome,Nhill Aerodrome,-36.3092,141.6486,138.9
omeo,Omeo,-37.1017,147.6008,689.8
orbost,Orbost,-37.6922,148.4667,62.65
port-fairy,Port Fairy AWS,-38.3906,142.2347,10
portland-airport,Portland (Cashmore Airport),-38.3148,141.4705,80.9
portland-harbour,Portland NTC AWS,-38.3439,141.6136,0
pound-creek,Pound Creek,-38.6297,145.8107,3
redesdale,Redesdale,-37.0194,144.5203,290
rhyll,Rhyll,-38.4612,145.3101,13.4
rutherglen,Rutherglen Research,-36.1047,146.5094,175
scoresby,Scoresby Research Institute,-37.871,145.2561,80
sheoaks,Sheoaks,-37.9075,144.1303,236.7
shepparton,Shepparton Airport,-36.4289,145.3947,113.9
stawell,Stawell Aerodrome,-37.072,142.7402,235.36
swan-hill,Swan Hill Aerodrome,-35.3766,143.5416,71
tatura,Tatura Inst Sustainable Ag,-36.4378,145.2672,114
viewbank,Viewbank,-37.7408,145.0972,66.1
kilmore-gap,Wallan (Kilmore Gap),-37.3807,144.9654,527.8
walpeup,Walpeup Research,-35.1201,142.004,105
wangaratta,Wangaratta Aero,-36.4206,146.3056,152.6
warrnambool,Warrnambool Airport NDB,-38.2867,142.4522,70.8
westmere,Westmere,-37.7067,142.9378,226
wilsons-promontory,Wilsons Promontory Lighthouse,-39.1297,146.4244,95
yarram-airport,Yarram Airport,-38.5647,146.7479,17.9
yarrawonga,Yarrawonga,-36.0294,146.0306,128.9"""

    buf = StringIO(string_of_observation_locations)

    loc_names = []
    list_of_csvs = []

    for i in buf:
        loc = str(i).replace('\n', '').split(',')
        loc_names.append(loc[0].lstrip())

    urladdy = "http://www.bom.gov.au/vic/observations/vicall.shtml"

    reader = urlopen(urladdy)

    full_page = StringIO(str(reader.read()))

    print "Scraping URL"
    for i in full_page:
        line = str(i).replace('\n','')

        for j in range(0,len(loc_names)):

            if loc_names[j] in line:

                if 'a href=' in line:
                    code = str(line).split('<')[2].split('>')[0].split('=')[1].split('.')[1]
                    list_of_csvs.append(("http://www.bom.gov.au/fwo/IDV60801/IDV60801." + str(code) +".axf", loc_names[j]))
    reader.close()
    for sites in list_of_csvs:
        print
        print "Starting for", sites[1]
        print "Sleeping, don't wake the baby"
        sleep(0.5)
        print "Wah wah wah"
        url_reader = urlopen(sites[0])
        line = url_reader.readline()
        while '[data]' not in line:
            line = url_reader.readline()
        csv_reader = csv.DictReader(url_reader)

        loc_obs = []
        for row in csv_reader:
            if row['name[80]']== None:
                continue
            code = sites[1]

            try:
                obs_time = arrow_get(row['local_date_time_full[80]'],'YYYYMMDDHHmmss', tzinfo='Australia/Melbourne')
            except ValueError:
                continue

            day_start = arrow_get(str(arrow_now().format('YYYY-MM-DD')) + " 00:00:00", 'YYYY-MM-DD HH:mm:ss',
                                  tzinfo='Australia/Melbourne').timestamp
            iter_time = arrow_get(obs_time).timestamp

            if iter_time < day_start:
                continue

            try:
                temp = float(row['air_temp'])
                if -50 < temp < 70:
                    pass
                else:
                    temp = "-"
            except ValueError:
                temp = "-"
            try:
                dew = float(row['dewpt'])
                if -50 < dew < 50:
                    pass
                else:
                    dew = "-"
            except ValueError:
                dew = "-"

            try:
                rain = float(row['rain_trace[80]'].replace('"',''))
                if 0 < rain < 400:
                    pass
                else:
                    rain = "0.0"
            except ValueError:
                rain = "0.0"

            try:
                pressure = float(row['press'])
                if 900 < pressure < 1100:
                    pass
                else:
                    pressure = "-"
            except ValueError:
                pressure = "-"

            try:
                rel_hum = int(row['rel_hum'])
                if -100 < rel_hum < 100:
                    pass
                else:
                    rel_hum = "-"
            except ValueError:
                rel_hum = "-"

            try:
                wind_vel = int(row['wind_spd_kmh'])
                if -1 < wind_vel < 300:
                    pass
                else:
                    wind_vel = "-"
            except ValueError:
                wind_vel = "-"

            try:
                wind_dir = row['wind_dir[80]']
            except ValueError:
                wind_dir = "-"

            try:
                lcl = 125 * (temp - dew)
            except TypeError:
                lcl = "-"

            loc_obs.insert(0, str(obs_time.timestamp) + ',' + str(temp) + ',' + str(dew) + ',' + str(rain) + ',' + str(pressure) + ',' + str(lcl) + ',' + str(rel_hum) + ',' + str(wind_vel) + ',' + wind_dir)

        for loc_line in loc_obs:
            file_time = arrow_get(loc_line.split(',')[0]).to('Australia/Melbourne').format('HH-mm')

        root_folder = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\"
        date_path = arrow_now().format('YYYY-MM-DD')

        try:
            chdir(root_folder + date_path)
        except WindowsError:
            mkdir(root_folder + date_path)

        try:
            chdir(root_folder + date_path + "\Observations")
        except WindowsError:
            mkdir(root_folder + date_path + "\Observations")

        filename = root_folder + date_path + "\Observations\\" + code + '.csv'

        with open(filename, 'w') as f:
            for loc_line in loc_obs:
                f.writelines(loc_line + '\n')



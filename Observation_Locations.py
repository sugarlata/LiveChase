from Observation_Location import ObservationLocation
import StringIO
import urllib


def give_me_vic_obs():

    string_of_observation_locations = """westmere,Westmere,-37.71,142.94,226
warrnambool,Warrnambool,-38.29,142.45,70.8
portland-harbour,Portland Harbour,-38.34,141.61,0
portland-airport,Portland Airport,-38.31,141.47,80.9
port-fairy,Port Fairy,-38.39,142.23,10
mount-william,Mount William,-37.3,142.6,1150
mount-gellibrand,Mount Gellibrand,-38.23,143.79,261
mortlake,Mortlake,-38.07,142.77,130
dartmoor,Dartmoor,-37.92,141.26,51
casterton,Casterton,-37.58,141.33,130.6
cape-otway,Cape Otway,-38.86,143.51,82
stawell,Stawell,-37.07,142.74,235.36
nhill-aerodrome,Nhill Aerodrome,-36.31,141.65,138.9
longerenong,Longerenong,-36.67,142.3,133
kanagulk,Kanagulk,-37.12,141.8,188.8
horsham,Horsham,-36.67,142.17,133.8
edenhope,Edenhope,-37.02,141.27,155
walpeup,Walpeup,-35.12,142,105
mildura,Mildura,-34.24,142.09,50
hopetoun-airport,Hopetoun Airport,-35.72,142.36,77.3
charlton,Charlton,-36.28,143.33,131.7
swan-hill,Swan Hill,-35.38,143.54,71
ben-nevis,Ben Nevis,-37.23,143.2,875
cape-nelson,Cape Nelson,-38.43,141.54,45.4
hamilton,Hamilton,-37.65,142.06,241.1
aireys-inlet,Aireys Inlet,-38.46,144.09,105
avalon,Avalon,-38.03,144.48,10.6
ballarat,Ballarat,-37.51,142.79,435.2
cerberus,Cerberus,-38.36,145.18,12.69
coldstream,Coldstream,-37.72,145.41,83
essendon-airport,Essendon Airport,-37.73,144.91,78.4
ferny-creek,Ferny Creek,-37.87,145.35,512.9
frankston,Frankston,-38.15,145.12,6
geelong-racecourse,Geelong Racecourse,-38.17,144.38,12.9
laverton,Laverton,-37.86,144.76,20.1
melbourne-airport,Melbourne Airport,-37.67,144.83,113.4
melbourne-olympic-park,Melbourne (Olympic Park),-37.83,144.98,7.53
moorabbin-airport,Moorabbin Airport,-37.98,145.1,12.1
pound-creek,Pound Creek,-38.63,145.81,3
rhyll,Rhyll,-38.46,145.31,13.4
scoresby,Scoresby,-37.87,145.26,80
sheoks,Sheoks,-37.91,144.13,236.7
viewbank,Viewbank,-37.71,145.1,66.1
bendigo,Bendigo,-36.74,144.33,208
kyabram,Kyabram,-36.34,145.06,105
mangalore,Mangalore,-36.89,145.19,140.8
redesdale,Redesdale,-37.02,144.52,290
shepparton,Shepparton,-36.43,145.39,113.9
tatura,Tatura,-38.44,145.27,114
yarrawonga,Yarrawonga,-36.03,146.03,128.9
albury,Albury,-34.08,146.95,163.5
falls-creek,Falls Creek,-36.87,147.28,1765
hunters-hill,Hunters Hill,-36.21,147.54,981
mount-buller,Mount Buller,-37.15,146.44,1707
mount-hotham-airport,Mount Hotham Airport,-37.05,147.33,1295.4
rutherglen,Rutherglen,-36.1,146.51,175
wangaratta,Wangaratta,-36.42,146.31,152.6
orbost,Orbost,-37.69,148.47,62.65
omeo,Omeo,-37.1,148.6,689.8
mount-nowa-nowa,Mount Nowa Nowa,-37.69,148.09,350
mallacoota,Mallacoota,-37.6,149.73,22
gelantipy,Gelantipy,-37.22,148.26,755
gabo-island,Gabo Island,-37.57,149.92,15.2
combienbar,Combienbar,-37.34,149.02,640
bairnsdale,Bairnsdale,-37.88,148.58,49.4
yarram-airport,Yarram Airport,-38.56,146.75,17.9
yanakie,Yanakie,-38.81,146.19,13.3
wilsons-promontory,Wilsons Promontory,-39.13,146.42,95
warragul-nilma-north,Warragul (Nilma North),-38.13,145.99,134.11
mount-moornapa,Mount Moornapa,-37.75,148.14,480
mount-baw-baw,Mount Baw Baw,-37.84,146.27,1561
latrobe-valley,Latrobe Valley,-38.21,146.47,55.7
hogan-island,Hogan Island,-39.22,146.98,116
east-sale,East Sale,-38.12,147.13,4.6
kilmore-gap,Kilmore Gap,-37.38,144.97,527.8
eildon-fire-tower,Eildon Fire Tower,-37.21,145.84,637"""

    buf = StringIO.StringIO(string_of_observation_locations)

    obs_list = []

    for i in buf:
        loc=str(i).replace('\n','').split(',')
        obs_list.append(ObservationLocation(loc[0].lstrip(),loc[1],float(loc[2]),float(loc[3]),float(loc[4])))

    urladdy = "http://www.bom.gov.au/vic/observations/vicall.shtml"

    reader = urllib.urlopen(urladdy)

    full_page = StringIO.StringIO(str(reader.read()))

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

    return obs_list

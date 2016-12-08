import serial
import arrow
import os
import simplekml
from pynmea import nmea


class GPS_Point:

    timestamp = int()
    time_formatted = ""
    lat = float
    lon = float

    def __init__(self, timestamp, time_formatted, lat,lon):

        self.timestamp = timestamp
        self.time_formatted = time_formatted
        self.lat = lat
        self.lon = lon


def create_gps_csv():
    print "Start"
    root_path = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\"
    print "Creating Object"
    ser = serial.Serial()
    ser.port = "COM4"
    ser.baudrate = 4800
    ser.bytesize = serial.EIGHTBITS
    ser.timeout = 1
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    print "Opening Port"
    ser.open()
    gpgga = nmea.GPGGA()

    year = arrow.now().format('YYYY')
    month = arrow.now().format('MM')
    day = arrow.now().format('DD')
    print "Receiving information"
    try:
        os.chdir(root_path + year + "-" + month + "-" + day)
    except WindowsError:
        os.mkdir(root_path + year + "-" + month + "-" + day)

    try:
        os.chdir(root_path + year + "-" + month + "-" + day + "\\GPS")
    except WindowsError:
        os.mkdir(root_path + year + "-" + month + "-" + day + "\\GPS")

    gps_path = root_path + year + "-" + month + "-" + day + "\\GPS"

    while True:
        data = ser.readline()

        if data[0:6] == '$GPGGA':
            print
            #  method for parsing the sentence
            gpgga.parse(data)

            lat = gpgga.latitude

            d = lat[:2]
            m = lat[2:4]
            s = float(lat[4:]) * 60

            if str(gpgga.lat_direction) == "S":
                d = "-" + d

            lat = str(d) + " " + str(m) + " " + str(s)

            lon = gpgga.longitude

            d = lon[:3]
            m = lon[3:5]
            s = float(lon[5:]) * 60

            if str(gpgga.lon_direction) == "W":
                d = "-" + d

            lon = str(d) + " " + str(m) + " " + str(s)


            time_stamp = gpgga.timestamp
            local_time = arrow.get(arrow.now('GMT').format('YYYY-MM-DD') + " " + arrow.get(time_stamp, 'HHmmss').format('HH:mm:ss'), 'YYYY-MM-DD HH:mm:ss').to('Australia/Melbourne')
            print "GPS time stamp : " + str(arrow.get(local_time).format('YYYY-MM-DD HH:mm:ss'))
            print lat, lon

            with open(gps_path + "\GPS.csv", 'a') as f:

                line_string = str(local_time) + "," + str(arrow.get(local_time).timestamp) + "," + str(lat) + "," + str(lon) + "\n"
                f.writelines(line_string)


def create_recent_kml():

    root_path = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\"
    date_path = arrow.now().format('YYYY-MM-DD')
    kml_file = "GPS Most Recent.kml"

    list_of_gps_obs = []

    with open(root_path + date_path + "\GPS\GPS.csv", 'r') as f:
        for line in f:
            splitline = line.split(',')
            lat = splitline[2].split(' ')
            latdec = str(lat[0]) + str((float(lat[1])/60)+(float(lat[2])/(60*60)))[1:]

            lon = splitline[3].split(' ')
            londec = str(lon[0]) + str((float(lon[1])/60)+(float(lon[2])/(60*60)))[1:]
            list_of_gps_obs.append(GPS_Point(int(splitline[1]),splitline[0],float(latdec),float(londec)))

    # filter list to most recent hour

    filtered_list_gps_obs = []

    for i in list_of_gps_obs:
        now_stamp = int(arrow.now().timestamp)
        if (now_stamp - 60*60) < i.timestamp < now_stamp:
            filtered_list_gps_obs.append(i)

    # Sort list

    filtered_list_gps_obs.sort(key=lambda x: x.timestamp)

    # create a kml

    when = []
    coordinates = []

    for i in filtered_list_gps_obs:
        when.append(i.time_formatted)
        coordinates.append([i.lon, i.lat])

    kml = simplekml.Kml(name="Live Chase GPS", open=1)

    doc = kml.newdocument(name='Live Chase GPS', snippet=simplekml.Snippet('Created ' + arrow.now().format('YYYY-MM-DD HH:mm:ss')))

    fol = doc.newfolder(name='Live GPS Track')

    schema = kml.newschema()

    trk = fol.newgxtrack(name='Track from past hour')

    trk.extendeddata.schemadata.schemaurl = schema.id

    trk.newwhen(when)
    trk.newgxcoord(coordinates)
    trk.stylemap.normalstyle.iconstyle.icon.href =\
        'http://earth.google.com/images/kml-icons/track-directional/track-0.png'
    trk.stylemap.normalstyle.linestyle.color = '99ffac59'
    trk.stylemap.normalstyle.linestyle.width = 6

    kml.save(root_path + date_path + "\GPS\\" + kml_file)

import serial
import string
from pynmea import nmea

ser = serial.Serial()
ser.port = "COM3"
ser.baudrate = 4800
ser.timeout = 1
ser.open()
gpgga = nmea.GPGGA()
while True:
    data = ser.readline()
    if data[0:6] == '$GPGGA':
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

        print lat, lon

        time_stamp = gpgga.timestamp
        print "GPS time stamp : " + str(time_stamp)

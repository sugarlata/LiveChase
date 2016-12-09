import os
import time
import arrow
import simplekml
import urllib2
from radar_db import RadarDB

from ftplib import FTP


def radar_kml(current_location):

    # Download Frames from BOM

    ftpaddy = 'ftp2.bom.gov.au'
    ftpcwd = '/anon/gen/radar/'
    framecode = ["024", "023", "022", "494", "493", "492", "02I", "49I"]

    root_path = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\"
    date_path = arrow.now().format('YYYY-MM-DD')

    try:
        os.chdir(root_path + date_path)
    except WindowsError:
        os.mkdir(root_path + date_path)

    try:
        os.chdir(root_path + date_path + "\\Radar")
    except WindowsError:
        os.mkdir(root_path + date_path + "\\Radar")

    ftpload = 1  # 0 = don't load, 1=do load

    if ftpload == 1:
        ftp = FTP(ftpaddy)
        ftp.login()
        ftp.cwd(ftpcwd)

        a = ftp.nlst()

        for b in range(0, len(framecode)):

            fl = []

            for i in range(0, len(a)):
                if a[i].find("IDR" + str(framecode[b])) != -1:
                    if a[i].find('.png') != -1:
                        fl.append(a[i])

            fl.sort()

            for fn in fl:

                try:
                    os.chdir(root_path + date_path + "\\Radar\\" + fn[:6])
                except WindowsError:
                    os.mkdir(root_path + date_path + "\\Radar\\" + fn[:6])

                try:
                    with open(fn) as f:
                        pass
                except IOError:
                    print "Downloading:", fn
                    gfile = open(fn, 'wb')
                    cmm = "RETR " + fn
                    ftp.retrbinary(cmm, gfile.write)
                    gfile.close()

        ftp.quit()

    frame_code_list = os.listdir(root_path + date_path + "\\Radar")
    print "Checked:", arrow.utcnow().to('Australia/Melbourne').format('HH:mm:ss')

    # Create the KML

    kml = simplekml.Kml()
    kml_folders = []

    ind = 0
    ground = []

    for k in frame_code_list:

        ground.insert(ind, [])

        if k[:3] == "IDR":

            kml_folders.append(kml.newfolder(name=k[:6]))

            radar_db = RadarDB(k[:6])

            idr_frame_list = os.listdir(root_path + date_path + "\\Radar\\" + k[:6])

            for i in range(0, len(idr_frame_list)):
                filename = idr_frame_list[i]
                idr_code = k[:6]

                frame_name = arrow.get(filename.split('.')[2], 'YYYYMMDDHHmm', tz='GMT').to('Australia/Melbourne').format('HH:mm')

                # Create a new ground overlay in kml_folders, keep this object in the 'ground' list.
                ground[ind].insert(i, kml_folders[ind].newgroundoverlay(name=frame_name))

                # Set the details for this ground overlay
                # What image will be over-layed
                ground[ind][i].icon.href = str(root_path + date_path + "\\Radar\\" + k[:6] + "\\" + filename).replace("//", "\\")
                radar_db.select_radar(idr_code[:-1] + "3")

                # What the position of the image will be
                ground[ind][i].latlonbox.north, ground[ind][i].latlonbox.south, ground[ind][i].latlonbox.east, ground[ind][i].latlonbox.west = \
                    radar_db.get_nsew(idr_code)

                pattern = "YYYYMMDDHHmm"
                str_time = arrow.get(filename.split('.')[2], pattern)
                epoch = str_time.timestamp

                # When the over-layed image will be shown and hidden
                ground[ind][i].timespan.begin = arrow.get(int(epoch))
                ground[ind][i].timespan.end = arrow.get(int(epoch) + 60*6)

                if i > 0:
                    ground[ind][i-1].visibility = 0
                    ground[ind][i-1].timespan.end = arrow.get(int(epoch))

        ind += 1

    os.chdir(root_path + date_path + "\\Radar")

    # Save the KML file
    kml.save("Radar.kml")
    print "KML Updated"


def satellite_kml():

    satellite_list = []

    user_agent = "live-chase/1.0"

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', user_agent)]
    response = opener.open("http://realtime.bsch.com.au/index.html?satmode=irenh1&region=melbourne&loop=yes&images=10&"
                           "allday=&start=&stop=#nav")
    page_line = response.readline()

    while True:

        if "tINm[9]" in page_line:

            satellite_list.append(str(page_line).split(' ')[2][:-3])

            break

        page_line = response.readline()

    while True:

        satellite_list.append(str(page_line).split(' ')[2][:-3])
        if 'tINm[0]' in page_line:
            break

        page_line = response.readline()

    print satellite_list

while True:
    # satellite_kml()
    radar_kml("")
    time.sleep(60)


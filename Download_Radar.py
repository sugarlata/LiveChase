import os
import time
import arrow
import simplekml
import urllib2
from radar_db import RadarDB

from ftplib import FTP



def radar_kml():

    # Download Frames from BOM

    ftpaddy = 'ftp2.bom.gov.au'
    ftpcwd = '/anon/gen/radar/'
    framecode = ["024", "023", "022"]
    localpathmain = "C://Users//Nathan//Documents//Storm Chasing//Radar Frames//"

    ftpload = 1  # 0 = don't load, 1=do load

    os.chdir(localpathmain)

    if ftpload == 1:
        ftp = FTP(ftpaddy)
        ftp.login()
        ftp.cwd(ftpcwd)

        a = []
        a = ftp.nlst()

        for b in range(0, len(framecode)):

            fl = []

            for i in range(0, len(a)):
                if a[i].find("IDR" + str(framecode[b])) != -1:
                    if a[i].find('.png') != -1:
                        fl.append(a[i])

                        """
                        try:
                            with open(a[i]) as f: pass
                        except IOError as e:
                            gFile=open(a[i], 'wb')
                            cmm = "RETR " + a[i]
                            ftp.retrbinary(cmm, gFile.write)
                            print "Frame Downloaded"
                            gFile.close()
                        """

            fl.sort()
            rayfra = fl[len(fl) - 1]

            try:
                with open(rayfra) as f:
                    pass
            except IOError as e:
                gFile = open(rayfra, 'wb')
                cmm = "RETR " + rayfra
                ftp.retrbinary(cmm, gFile.write)
                gFile.close()

        ftp.quit()

    frame_filename_list = os.listdir(localpathmain)
    print "Checked:", arrow.utcnow().to('Australia/Melbourne').format('HH:mm:ss')

    idr024=[]
    idr022=[]
    idr023=[]

    for i in range(0, len(frame_filename_list)):
        if str(frame_filename_list[i][:6]) == "IDR024":
            idr024.append(frame_filename_list[i])
        if str(frame_filename_list[i][:6]) == "IDR023":
            idr023.append(frame_filename_list[i])
        if str(frame_filename_list[i][:6]) == "IDR022":
            idr022.append(frame_filename_list[i])

    kml = simplekml.Kml()
    kml_folders = []

    kml_folders.append(kml.newfolder(name="IDR024"))
    ground24 =[]

    radar_db = RadarDB("IDR023")

    for i in range(0, len(idr024)):
        filename = idr024[i]
        idr_code = "IDR024"

        # Create a new ground overlay in kml_folders, keep this object in the 'ground' list.
        ground24.insert(len(ground24), kml_folders[0].newgroundoverlay(name=filename.split('.')[2]))

        # Set the details for this ground overlay
        # What image will be over-layed
        ground24[i].icon.href = str(localpathmain + filename).replace("//", "\\")
        radar_db.select_radar(idr_code[:-1] + "3")

        # What the position of the image will be
        ground24[i].latlonbox.north, ground24[i].latlonbox.south, ground24[i].latlonbox.east, ground24[i].latlonbox.west = \
            radar_db.get_nsew(idr_code)

        pattern = "YYYYMMDDHHmm"
        time = arrow.get(filename.split('.')[2], pattern)
        epoch = time.timestamp

        # When the over-layed image will be shown and hidden
        ground24[i].timespan.begin = arrow.get(int(epoch))
        ground24[i].timespan.end = arrow.get(int(epoch) + 360)








    kml_folders.append(kml.newfolder(name="IDR023"))
    ground23 =[]

    radar_db = RadarDB("IDR023")

    for i in range(0, len(idr023)):
        filename = idr023[i]
        idr_code = "IDR023"

        # Create a new ground overlay in kml_folders, keep this object in the 'ground' list.
        ground23.insert(len(ground23), kml_folders[1].newgroundoverlay(name=filename.split('.')[2]))

        # Set the details for this ground overlay
        # What image will be over-layed
        ground23[i].icon.href = str(localpathmain + filename).replace("//", "\\")
        radar_db.select_radar(idr_code[:-1] + "3")

        # What the position of the image will be
        ground23[i].latlonbox.north, ground23[i].latlonbox.south, ground23[i].latlonbox.east, ground23[i].latlonbox.west = \
            radar_db.get_nsew(idr_code)

        pattern = "YYYYMMDDHHmm"
        time = arrow.get(filename.split('.')[2], pattern)
        epoch = time.timestamp

        # When the over-layed image will be shown and hidden
        ground23[i].timespan.begin = arrow.get(int(epoch))
        ground23[i].timespan.end = arrow.get(int(epoch) + 360)








    kml_folders.append(kml.newfolder(name="IDR022"))
    ground22 =[]

    radar_db = RadarDB("IDR022")

    for i in range(0, len(idr022)):
        filename = idr022[i]
        idr_code = "IDR022"

        # Create a new ground overlay in kml_folders, keep this object in the 'ground' list.
        ground22.insert(len(ground22), kml_folders[2].newgroundoverlay(name=filename.split('.')[2]))

        # Set the details for this ground overlay
        # What image will be over-layed
        ground22[i].icon.href = str(localpathmain + filename).replace("//", "\\")
        radar_db.select_radar(idr_code[:-1] + "3")

        # What the position of the image will be
        ground22[i].latlonbox.north, ground22[i].latlonbox.south, ground22[i].latlonbox.east, ground22[i].latlonbox.west = \
            radar_db.get_nsew(idr_code)

        pattern = "YYYYMMDDHHmm"
        time = arrow.get(filename.split('.')[2], pattern)
        epoch = time.timestamp

        # When the over-layed image will be shown and hidden
        ground22[i].timespan.begin = arrow.get(int(epoch))
        ground22[i].timespan.end = arrow.get(int(epoch) + 360)









    os.chdir(localpathmain)

    # Save the KML file
    kml.save("Radar.kml")


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
    radar_kml()
    time.sleep(60)


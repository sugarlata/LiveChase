from Incident_Objects import Incident
import json
import urllib2
import arrow
from pprint import pprint
import simplekml
from StringIO import StringIO
import gzip
import os

def create_incidents_kml():

    # If variable below is 0, is unconditional
    incidents_from_last_x_hours = 8

    incidents_lists=[]

    formatted_time = arrow.now().format('YYYY-MM-DD HH.mm.ss')

    root_folder = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\"
    date_path = arrow.now().format('YYYY-MM-DD')

    urladdy = "http://emergency.vic.gov.au/public/osom-geojson.json"

    request = urllib2.Request(urladdy)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        response_data = f.read()

    d = json.loads(response_data)

    for i in range(0, len(d["features"])):

        if d["features"][i]["geometry"]["type"] == "Point":

            try:
                lat = float(d["features"][i]["geometry"]["coordinates"][1])
                lon = float(d["features"][i]["geometry"]["coordinates"][0])
                source = d["features"][i]["properties"]["sourceOrg"]
                source_title = d["features"][i]["properties"]["sourceTitle"]
                category1 = d["features"][i]["properties"]["category1"]
                category2 = d["features"][i]["properties"]["category2"]
                created = d["features"][i]["properties"]["created"]
                id_tag = d["features"][i]["properties"]["id"]
                location = d["features"][i]["properties"]["location"]
                resources = d["features"][i]["properties"]["resources"]
                status = d["features"][i]["properties"]["status"]

                if incidents_from_last_x_hours == 0:
                    incidents_lists.append(Incident(lat, lon, source, source_title, category1, category2, created,
                                                    id_tag, location, resources, status))
                    print i, "Unlimited"

                else:
                    back_limit = arrow.now().timestamp - (incidents_from_last_x_hours * 60 * 60)
                    if int(arrow.get(created).timestamp) > int(back_limit):
                        incidents_lists.append(Incident(lat, lon, source, source_title, category1, category2, created,
                                                        id_tag, location, resources, status))
                        print i, "Limited"

            except KeyError:

                print
                print "Some issue with one of the points, this point will not be appended"
                print i
                pprint(d["features"][i])

    kml = simplekml.Kml()

    incident_folder = kml.newfolder(name='Incidents')

    points_list=[]

    description_html = r"""<![CDATA[<font size = "4">
    ID: $ID$</font><br>
    <font size = "4">
    Created: $CREATED$</font><br>
    <font size = "4">
    Location: $LOCATION$</font><br>
    <font size = "4">
    Status: $STATUS$</font><br>
    <font size = "4">
    Source: $SOURCE$</font><br>
    <font size = "4">
    Source Title: $SOURCE_TITLE$</font><br>
    <font size = "4">
    Category 1: $CAT1$</font><br>
    <font size = "4">
    Category 2: $CAT2$</font><br>
    <font size = "4">
    Resources: $RESOURCES$</font><br>
    <font size = 4><br><br></font>]]>"""

    for i in range(0, len(incidents_lists)):

        current_incident = incidents_lists[i]

        points_list.append(incident_folder.newpoint(name=str(current_incident.get_category1())))
        points_list[i].timespan.begin = arrow.get(current_incident.get_created())
        points_list[i].timespan.end = arrow.now()

        lat = incidents_lists[i].get_lat_lon()[0]
        lon = incidents_lists[i].get_lat_lon()[1]
        points_list[i].coords = [(lon, lat)]

        points_list[i].style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/paddle/red-stars.png"

        str_id = str(current_incident.get_id())
        str_source = current_incident.get_source()
        str_source_title = current_incident.get_source_title()
        str_cat1 = current_incident.get_category1()
        str_cat2 = current_incident.get_category2()
        str_created = current_incident.get_created()
        str_location = current_incident.get_location()
        str_resources = str(current_incident.get_resources())
        str_status = current_incident.get_status()

        str_created_formatted = arrow.get(str_created).to('Australia/Melbourne').format('DD/MM/YY   HH:mm')

        points_list[i].description = description_html.replace('$ID$', str_id).replace('$SOURCE$', str_source).replace('$SOURCE_TITLE$', str_source_title).replace('$CAT1$', str_cat1).replace('$CAT2$', str_cat2).replace('$CREATED$', str_created_formatted).replace('$LOCATION$', str_location).replace('$RESOURCES$', str_resources).replace('$STATUS$', str_status)

    incident_folder2 = kml.newfolder(name='Incidents offset an hour earlier')

    points_list2=[]

    for i in range(0, len(incidents_lists)):

        current_incident = incidents_lists[i]

        points_list2.append(incident_folder2.newpoint(name=str(current_incident.get_category1())))

        points_list2[i].timespan.begin = arrow.get(current_incident.get_created() - (60 * 60))
        points_list2[i].timespan.end = arrow.get(current_incident.get_created() + (60*60))

        lat = incidents_lists[i].get_lat_lon()[0]
        lon = incidents_lists[i].get_lat_lon()[1]
        points_list2[i].coords = [(lon, lat)]

        points_list2[i].style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/paddle/red-stars.png"
        points_list2[i].visibility = 0

    try:
        os.chdir(root_folder + date_path)
    except WindowsError:
        os.mkdir(root_folder + date_path)

    try:
        os.chdir(root_folder + date_path + "\Incidents")
    except WindowsError:
        os.mkdir(root_folder + date_path + "\Incidents")

    live_save = root_folder + date_path + "\Incidents\Incidents Most Recent.kml"
    backup_save = root_folder + date_path + "\Incidents\Incidents " + formatted_time + ".kml"

    kml.save(live_save)
    kml.save(backup_save)


if __name__ == '__main__':
    create_incidents_kml()

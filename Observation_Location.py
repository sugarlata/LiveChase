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


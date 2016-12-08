import arrow


class Incident:

    __lat__ = float()
    __lon__ = float()
    __source__ = ""
    __source_title__ = ""
    __category1__ = ""
    __category2__ = ""
    __created__ = ""
    __id__ = ""
    __location__ = ""
    __resources__ = ""
    __status__ = ""

    def __init__(self, lat, lon, source, source_title, category1, category2, created, id_point, location, resources,
                 status):

        self.__lat__ = lat
        self.__lon__ = lon
        self.__source__ = source
        self.__source_title__ = source_title
        self.__category1__ = category1
        self.__category2__ = category2
        self.__created__ = arrow.get(created).timestamp
        self.__id__ = id_point
        self.__location__ = location
        self.__resources__ = resources
        self.__status__ = status

    def set_lat_lon(self, lat, lon):

        self.__lat__ = lat
        self.__lon__ = lon

    def set_source(self, source):

        self.__source__ = source

    def set_source_title(self, source_title):

        self.__source_title__ = source_title

    def set_category1(self, category1):

        self.__category1__ = category1

    def set_category2(self, category2):

        self.__category2__ = category2

    def set_created(self, created):

        self.__created__ = created

    def set_id(self, id_tag):

        self.__id__ = id_tag

    def set_location(self, location):

        self.__location__ = location

    def set_resources(self, resources):

        self.__resources__ = resources

    def set_status(self, status):

        self.__status__ = status

    def get_lat_lon(self):

        return self.__lat__, self.__lon__

    def get_source(self):

        return self.__source__

    def get_source_title(self):

        return self.__source_title__

    def get_category1(self):

        return self.__category1__

    def get_category2(self):

        return self.__category2__

    def get_created(self):

        return self.__created__

    def get_id(self):

        return self.__id__

    def get_location(self):

        return self.__location__

    def get_resources(self):

        return self.__resources__

    def get_status(self):

        return self.__status__



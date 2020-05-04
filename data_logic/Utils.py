from datetime import datetime
from math import radians, sin, cos, sqrt, atan2


class Utils:
    @staticmethod
    def convert_to_unix_time(date_string: str) -> str:
        date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
        unix_date = (date - datetime(1970, 1, 1)).total_seconds()
        return str(int(unix_date))

    @staticmethod
    def convert_cords_to_distance(lat1: str, lon1: str, lat2: str, lon2: str) -> str:
        earth_radius = 6373.0
        lat1 = radians(float(lat1))
        lon1 = radians(float(lon1))
        lat2 = radians(float(lat2))
        lon2 = radians(float(lon2))

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = earth_radius * c
        return str(distance)

from datetime import datetime
from math import radians, sin, cos, sqrt, atan2


class Utils:
    @staticmethod
    def convert_to_unix_time(date_string: str) -> int:
        date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
        unix_date = (date - datetime(1970, 1, 1)).total_seconds()
        return int(unix_date)

    @staticmethod
    def get_difference_between_unix_time(unix_time_one: int, unix_time_two: int) -> int:
        return abs(unix_time_one - unix_time_two)

    @staticmethod
    def convert_cords_to_distance(lat1: str, lon1: str, lat2: str, lon2: str) -> int:
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
        return int(round(distance))

    @staticmethod
    def round_unix_time_to_full_hours(unix_time: int) -> float:
        if unix_time % 3600 > 1800:
            result = unix_time + 3600 - (unix_time % 3600)  # unix time rounded to full hours (ceiled)
        else:
            result = unix_time - unix_time % 3600  # unix time rounded to full hours (floored)
        return float(result) / 3600  # unix time converted to full hours

    @staticmethod
    def split_zip_code(zip_code: str):
        temp_zip = zip_code.split("-")[0]
        return temp_zip[0], temp_zip[1]

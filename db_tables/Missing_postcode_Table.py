import mysql.connector
from aifc import Error
from mysql.connector import pooling
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from data_logic.SingleRecord import SingleRecord
from db_tables.Postcode_Table import Postcode_Table


class Missing_postcode_Table:
    def __init__(self, cnx_pool: mysql.connector.pooling):
        self.cnx_pool = cnx_pool
        self.table_name = "missing_postcode"

    def __del__(self):
        pass

    def check_if_record_exists(self, zip_code: str, country_code: str) -> bool:
        cnx = self.cnx_pool.get_connection()
        cursor = cnx.cursor()
        record_exist = True
        sql_query = "SELECT * FROM {} WHERE zip_code = '{}' AND country_code = '{}' LIMIT 0, 1".format(
            self.table_name, zip_code, country_code)

        try:
            cursor.execute(sql_query)
            result = cursor.fetchone()
            if result is None:
                record_exist = False
        except mysql.connector.Error as err:
            # TODO: work on exception
            print(err)
            exit(1)

        cursor.close()
        cnx.close()
        return record_exist

    def insert_record(self, zip_code: str, country_code: str):
        cnx = self.cnx_pool.get_connection()
        cursor = cnx.cursor()
        sql_query = "INSERT INTO {} (zip_code, country_code) VALUES ('{}', '{}')".format(
            self.table_name, zip_code, country_code)

        try:
            cursor.execute(sql_query)
        except mysql.connector.Error as err:
            # TODO: work on exception
            print(err)
            exit(1)

        cnx.commit()
        cursor.close()
        cnx.close()

    def handle_missing_record(self, sr: SingleRecord):
        if not sr.receiver_zip_found and not sr.sender_zip_found:
            receiver_record_exists = self.check_if_record_exists(sr.receiver_zip, sr.receiver_country_code)
            sender_record_exists = self.check_if_record_exists(sr.sender_zip, sr.sender_country_code)
            if not receiver_record_exists:
                self.insert_record(sr.receiver_zip, sr.receiver_country_code)
            if not sender_record_exists:
                self.insert_record(sr.sender_zip, sr.sender_country_code)
        elif not sr.receiver_zip_found:
            receiver_record_exists = self.check_if_record_exists(sr.receiver_zip, sr.receiver_country_code)
            if not receiver_record_exists:
                self.insert_record(sr.receiver_zip, sr.receiver_country_code)
        elif not sr.sender_zip_found:
            sender_record_exists = self.check_if_record_exists(sr.sender_zip, sr.sender_country_code)
            if not sender_record_exists:
                self.insert_record(sr.sender_zip, sr.sender_country_code)

    def update_dictionary_with_missing_postcodes(self, seconds_delay: int = 3):
        cnx = self.cnx_pool.get_connection()
        cursor = cnx.cursor()
        sql_query = "SELECT * FROM {}".format(self.table_name)
        postcode_table = Postcode_Table(self.cnx_pool)

        try:
            cursor.execute(sql_query)
            records = cursor.fetchall()
            geolocator = Nominatim(user_agent="Wojtas")
            geocode = RateLimiter(geolocator.geocode, min_delay_seconds=seconds_delay, max_retries=20, error_wait_seconds=10.0)
            reverse = RateLimiter(geolocator.reverse, min_delay_seconds=seconds_delay, max_retries=20, error_wait_seconds=10.0)
            for row in records:
                postcode = row[1]
                country_code = row[2]
                location_string = postcode + " " + country_code

                location = geocode(location_string)
                reversed_location = reverse((location.latitude, location.longitude))

                address = reversed_location.raw['address']

                place = address.get('city')
                if place is None:
                    place = address.get('town')
                    if place is None:
                        place = address.get('village')
                state = address.get('state')
                county = address.get('county')
                municipality = address.get('municipality')
                if municipality is None:
                    municipality = place
                success = postcode_table.insert_new_location(country_code, postcode, place, state, county, municipality,
                                                             location.latitude, location.longitude, '8.0')
                if success:
                    self.remove_single_record(postcode)
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if cnx.is_connected():
                cursor.close()
                cnx.close()

    def remove_single_record(self, postcode: str):
        cnx = self.cnx_pool.get_connection()
        cursor = cnx.cursor()
        sql_query = "DELETE FROM {} WHERE zip_code = '{}'".format(self.table_name, postcode)

        try:
            cursor.execute(sql_query)
            cnx.commit()
            print("--- postcode: " + postcode + " removed from " + self.table_name + " successfully---")
        except Error as e:
            print("Error while deleting data from MySQL table", e)
        finally:
            if cnx.is_connected():
                cursor.close()
                cnx.close()

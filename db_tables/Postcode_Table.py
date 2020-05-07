import mysql.connector
import pandas as pd
from mysql.connector import Error
from mysql.connector import pooling


class Postcode_Table:
    def __init__(self, cnx_pool: mysql.connector.pooling, table_name: str = "postcode_table"):
        self.cnx_pool = cnx_pool
        self.table_name = table_name
        pass

    def __del__(self):
        pass

    def fill_table(self, path: str, rows=-1, separator="\t", ):
        cnx = self.cnx_pool.get_connection()
        cursor = cnx.cursor()
        # headings = ['country_code', 'postal_code', 'place_name', 'admin_name1', 'admin_code1',
        #             'admin_name2', 'admin_code2', 'admin_name3', 'admin_code3', 'latitude',
        #             'longitude', 'accuracy']

        if rows < 0:
            df = pd.read_csv(path, sep=separator)
        else:
            df = pd.read_csv(path, sep=separator, nrows=rows)
        for index, row in df.iterrows():
            query_insert = ("INSERT INTO `{}` (`ID`, `country_code`, `postal_code`, `place_name`, `admin_name1`, "
                            "`admin_code1`, `admin_name2`, `admin_code2`, `admin_name3`, `admin_code3`,"
                            " `latitude`, `longitude`, `accuracy`) "
                            "VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}', '{}', "
                            "'{}', '{}', '{}', '{}', '{}');").format(self.table_name,
                                                                     row['country_code'], row['postal_code'],
                                                                     row['place_name'],
                                                                     row['admin_name1'], row['admin_code1'],
                                                                     row['admin_name2'], row['admin_code2'],
                                                                     row['admin_name3'], row['admin_code3'],
                                                                     row['latitude'], row['longitude'], row['accuracy'])
            cursor.execute(query_insert)
        cnx.commit()
        cursor.close()
        cnx.close()

    def get_coordinates(self, country_code: str, post_code: str) -> dict:
        coord = dict()
        cnx = self.cnx_pool.get_connection()
        cursor = cnx.cursor()
        sql_query = "SELECT *  FROM `postcode_table` WHERE `country_code` LIKE '{}' AND `postal_code` LIKE " \
                    "'{}' ORDER BY `country_code` DESC LIMIT 0, 1".format(country_code, post_code)
        try:
            cursor.execute(sql_query)
            result = cursor.fetchone()

            if result is None:
                coord['empty'] = True
            else:
                coord['empty'] = False
                coord['placeName'] = result[3]
                coord['latitude'] = "{:.4f}".format(result[10])
                coord['longitude'] = "{:.4f}".format(result[11])
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if cnx.is_connected():
                cursor.close()
                cnx.close()
        return coord

    def insert_new_location(self, country_code, postal_code, place_name, admin_name1, admin_name2, admin_name3,
                            latitude, longitude, accuracy) -> bool:
        success = False
        cnx = self.cnx_pool.get_connection()
        cursor = cnx.cursor()
        sql_query = "INSERT INTO {} (country_code, postal_code, place_name, admin_name1, admin_code1, admin_name2, " \
                    "admin_code2, admin_name3, admin_code3, latitude, longitude, accuracy) " \
                    "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            self.table_name, country_code, postal_code, place_name, admin_name1, 0, admin_name2, 0, admin_name3, 0,
            latitude, longitude, accuracy)
        try:
            cursor.execute(sql_query)
            cnx.commit()
            success = True
            print("--- postcode: " + postal_code + " inserted into " + self.table_name + " successfully---")
        except Error as e:
            print("Error while inserting data to MySQL table", e)
        finally:
            if cnx.is_connected():
                cursor.close()
                cnx.close()
        return success

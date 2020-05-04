import mysql.connector
import pandas as pd
from mysql.connector import Error
from data_db_connector.DBConnector import DBConnector


class Postcode_Table:

    def __init__(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def fill_table(path: str, table_name: str, database_name: str = "", rows=-1, separator="\t", ):

        dbc = DBConnector()
        cnx = dbc.create_Connection()
        if database_name == "":
            cnx.database = dbc.database
        else:
            cnx.database = database_name
        cursor = cnx.cursor()
        headings = ['country_code', 'postal_code', 'place_name', 'admin_name1', 'admin_code1',
                    'admin_name2', 'admin_code2', 'admin_name3', 'admin_code3', 'latitude',
                    'longitude', 'accuracy']

        df = pd
        if rows < 0:
            df = pd.read_csv(path, sep=separator)
        else:
            df = pd.read_csv(path, sep=separator, nrows=rows)
        for index, row in df.iterrows():
            query_insert = ("INSERT INTO `{}` (`ID`, `country_code`, `postal_code`, `place_name`, `admin_name1`, "
                            "`admin_code1`, `admin_name2`, `admin_code2`, `admin_name3`, `admin_code3`,"
                            " `latitude`, `longitude`, `accuracy`) "
                            "VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}', '{}', "
                            "'{}', '{}', '{}', '{}', '{}');").format(table_name,
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

    @staticmethod
    def getCoordinates(country_code: str, post_code: str, database_name: str = ""):
        coord = dict()
        try:
            sql_select_Query = "SELECT *  FROM `postcode_table` WHERE `country_code` LIKE '{}' AND `postal_code` LIKE " \
                               "'{}' ORDER BY `country_code`  DESC".format(country_code, post_code)
            dbc = DBConnector()
            cnx = dbc.create_Connection()
            if database_name == "":
                cnx.database = dbc.database
            else:
                cnx.database = database_name
            cursor = cnx.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()

            if cursor.rowcount > 0:
                coord['empty'] = False
                coord['placeName'] = records[0][3]
                coord['latitude'] = records[0][10]
                coord['longitude'] = records[0][11]
            else:
                coord['empty'] = True
                coord['post-code'] = post_code

        except Error as e:
            print("Error reading data from MySQL table", e)

        finally:
            if (cnx.is_connected()):
                cnx.close()
                cursor.close()
                print("MySQL connection is closed")

        return coord

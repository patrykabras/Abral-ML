import mysql.connector
from mysql.connector import pooling

from data_logic.SingleRecord import SingleRecord


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

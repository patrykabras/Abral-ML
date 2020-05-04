import mysql

from data_db_connector.DBConnector import DBConnector
from data_logic.SingleRecord import SingleRecord


class Missing_postcode_Table:

    def __init__(self, db_connector: DBConnector):
        self.dbc = db_connector
        self.table_name = "missing_postcode"
        pass

    def __del__(self):
        pass

    def check_if_record_exists(self, zip_code: str, country_code: str) -> bool:
        db_name = self.dbc.database
        cnx = self.dbc.create_Connection()
        cursor = cnx.cursor()
        record_exist = True

        try:
            cursor.execute("USE {}".format(db_name))
            cursor.execute("SELECT * FROM {} "
                           "WHERE zip_code = '{}' AND "
                           "country_code = '{}'".format(
                            self.table_name, zip_code, country_code))
            records = cursor.fetchall()
            if cursor.rowcount == 0:
                record_exist = False
        except mysql.connector.Error as err:
            # TODO: work on exception
            print(err)
            exit(1)

        cnx.commit()
        cursor.close()
        cnx.close()
        return record_exist

    def insertRecord(self, zip_code: str, country_code: str):
        db_name = self.dbc.database
        cnx = self.dbc.create_Connection()
        cursor = cnx.cursor()

        try:
            cursor.execute("USE {}".format(db_name))
            cursor.execute("INSERT INTO {} (zip_code, country_code) "
                           "VALUES ('{}', '{}')".format(
                            self.table_name, zip_code, country_code))
        except mysql.connector.Error as err:
            # TODO: work on exception
            print(err)
            exit(1)

        cnx.commit()
        cursor.close()
        cnx.close()
        pass

    def handle_missing_record(self, sr: SingleRecord):
        if not sr.receiver_zip_found and not sr.sender_zip_found:
            receiver_record_exists = self.check_if_record_exists(sr.receiver_zip, sr.receiver_country_code)
            sender_record_exists = self.check_if_record_exists(sr.sender_zip, sr.sender_country_code)
            if not receiver_record_exists:
                self.insertRecord(sr.receiver_zip, sr.receiver_country_code)
            if not sender_record_exists:
                self.insertRecord(sr.sender_zip, sr.sender_country_code)
        elif not sr.receiver_zip_found:
            receiver_record_exists = self.check_if_record_exists(sr.receiver_zip, sr.receiver_country_code)
            if not receiver_record_exists:
                self.insertRecord(sr.receiver_zip, sr.receiver_country_code)
        elif not sr.sender_zip_found:
            sender_record_exists = self.check_if_record_exists(sr.sender_zip, sr.sender_country_code)
            if not sender_record_exists:
                self.insertRecord(sr.sender_zip, sr.sender_country_code)
        pass

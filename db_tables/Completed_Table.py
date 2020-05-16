import mysql.connector
import numpy
from mysql.connector import pooling

from data_logic.SingleRecord import SingleRecord


class Completed_Table:

    def __init__(self, cnx_pool: mysql.connector.pooling):
        self.cnx_pool = cnx_pool
        self.table_name = "completed"

    def __del__(self):
        pass

    def insert_record(self, sr: SingleRecord, contract_type_id: str):
        cnx = self.cnx_pool.get_connection()
        cursor = cnx.cursor()

        insert_record_query = ("INSERT INTO `{}` "
                               "(`shipment_identcode`, "
                               "`contract_type_id`, "
                               "`shipment_createdate`, "
                               "`unix_shipment_createdate`, "
                               "`first_event`, "
                               "`unix_first_event`, "
                               "`last_event`, "
                               "`unix_last_event`, "
                               "`unix_difference`, "
                               "`receiver_country_code`, "
                               "`receiver_city_name`, "
                               "`receiver_zip`, "
                               "`receiver_latitude`, "
                               "`receiver_longitude`, "
                               "`sender_country_code`, "
                               "`sender_city_name`, "
                               "`sender_zip`, "
                               "`sender_latitude`, "
                               "`sender_longitude`, "
                               "`distance`) "
                               "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', "
                               "'{}', '{}', '{}', '{}', '{}', '{}')").format(
            self.table_name,
            sr.shipment_identicode,
            contract_type_id,
            sr.shipment_createdate,
            sr.unix_shipment_createdate,
            sr.first_event,
            sr.unix_first_event,
            sr.last_event,
            sr.unix_last_event,
            sr.unix_difference,
            sr.receiver_country_code,
            sr.receiver_city_name,
            sr.receiver_zip,
            sr.receiver_latitude,
            sr.receiver_longitude,
            sr.sender_country_code,
            sr.sender_city_name,
            sr.sender_zip,
            sr.sender_latitude,
            sr.sender_longitude,
            sr.distance)

        try:
            cursor.execute(insert_record_query)
        except mysql.connector.Error as err:
            # TODO: work on exception
            print("Table {} does not exists.".format(self.table_name))
            print(err)
            exit(1)

        cnx.commit()
        cursor.close()
        cnx.close()

    def collect_data(self, start_from: int = 0, rows: int = 1000) -> numpy:
        cnx = self.cnx_pool.get_connection()
        cursor = cnx.cursor()
        sql_query = "SELECT unix_difference, unix_shipment_createdate, distance, sender_zip , receiver_zip distance FROM {} LIMIT {}, {}".format(
            self.table_name, start_from, rows)
        data = None

        try:
            cursor.execute(sql_query)
            results = cursor.fetchall()

            data = numpy.empty((rows,), dtype=[('', numpy.uint32)] * 7)
            i = 0
            for cell in results:
                tempZip: str = cell[3]
                tempZip = tempZip.split("-")[0]
                tempZip1: str = cell[4]
                tempZip1 = tempZip1.split("-")[0]

                data[i][1] = cell[1]
                data[i][2] = cell[2]
                data[i][3] = tempZip[0]
                data[i][4] = tempZip[1]
                data[i][5] = tempZip1[0]
                data[i][6] = tempZip1[1]
                if cell[0] % 3600 > 1800:
                    data[i][0] = cell[0] + 3600 - (cell[0] % 3600)  # unix time rounded to full hours (ceiled)
                else:
                    data[i][0] = cell[0] - cell[0] % 3600  # unix time rounded to full hours (floored)
                data[i][0] = float(cell[0]) / 3600  # unix time converted to hours
                print(data[i])
                i = i + 1

            data = data.view(numpy.int32).reshape(-1, 7)

        except mysql.connector.Error as err:
            # TODO: work on exception
            print("Table {} does not exists.".format(self.table_name))
            print(err)
            exit(1)
        cnx.commit()
        cursor.close()
        cnx.close()
        return data

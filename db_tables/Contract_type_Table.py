import mysql.connector
from mysql.connector import pooling


class Contract_type_Table:
    def __init__(self, cnx_pool: mysql.connector.pooling) -> None:
        self.cnx_pool = cnx_pool
        self.table_name = "contract_type"

    def __del__(self):
        pass

    def get_contract_type_id(self, contract_type: str, xlidentifier: str) -> str:
        cnx = self.cnx_pool.get_connection()
        cursor = cnx.cursor()
        contract_type_id = None
        sql_query = "SELECT * FROM {} WHERE Name = '{}' AND XLIDENTIFIER = '{}' LIMIT 0, 1".format(
            self.table_name, contract_type, xlidentifier)

        try:
            cursor.execute(sql_query)
            result = cursor.fetchone()
            if result is None:
                contract_type_id = self.insert_record(contract_type, xlidentifier)
            else:
                contract_type_id = result[0]
        except mysql.connector.Error as err:
            # TODO: work on exception
            print("Table {} does not exists.".format(self.table_name))
            print(err)
            exit(1)

        cursor.close()
        cnx.close()
        return contract_type_id

    def insert_record(self, contract_type: str, xlidentifier: str) -> str:
        cnx = self.cnx_pool.get_connection()
        cursor = cnx.cursor()
        sql_query = "INSERT INTO {} (Name, XLIDENTIFIER) VALUES ('{}', '{}')".format(
                            self.table_name, contract_type, xlidentifier)

        try:
            cursor.execute(sql_query)
        except mysql.connector.Error as err:
            # TODO: work on exception
            print(err)
            exit(1)

        cnx.commit()
        cursor.close()
        cnx.close()
        # returning id of the inserted row
        return cursor.lastrowid

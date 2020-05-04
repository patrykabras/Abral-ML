import mysql.connector
from mysql.connector import errorcode
from data_db_connector.DBConnector import DBConnector


class Contract_type_Table:

    def __init__(self, db_connector: DBConnector):
        self.dbc = db_connector
        self.table_name = "contract_type"
        pass

    def __del__(self):
        pass

    def check_if_contract_type_exists(self, contract_type: str, xlidentifier: str) -> str:
        db_name = self.dbc.database
        cnx = self.dbc.create_Connection()
        cursor = cnx.cursor()
        contract_type_id = None

        try:
            cursor.execute("USE {}".format(db_name))
            cursor.execute("SELECT * FROM {} "
                           "WHERE Name = '{}' "
                           "AND XLIDENTIFIER = '{}'".format(
                            self.table_name, contract_type, xlidentifier))
            records = cursor.fetchall()
            if cursor.rowcount == 0:
                return self.insert_record(contract_type, xlidentifier)
            else:
                for row in records:
                    contract_type_id = row[0]
        except mysql.connector.Error as err:
            # TODO: work on exception
            print("Table {} does not exists.".format(self.table_name))
            print(err)
            exit(1)

        cnx.commit()
        cursor.close()
        cnx.close()

        return contract_type_id

    def insert_record(self, contract_type: str, xlidentifier: str) -> str:
        db_name = self.dbc.database
        cnx = self.dbc.create_Connection()
        cursor = cnx.cursor()

        try:
            cursor.execute("USE {}".format(db_name))
            cursor.execute("INSERT INTO {} (Name, XLIDENTIFIER) "
                           "VALUES ('{}', '{}')".format(
                            self.table_name, contract_type, xlidentifier))
        except mysql.connector.Error as err:
            # TODO: work on exception
            print(err)
            exit(1)

        cnx.commit()
        cursor.close()
        cnx.close()

        return cursor.lastrowid

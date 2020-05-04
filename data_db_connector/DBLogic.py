import mysql.connector
from mysql.connector import errorcode
from data_db_connector.DBConnector import DBConnector


class DBLogic:

    def __init__(self, db_connector: DBConnector, dictionary_table: str = "contract_type", completed_table: str = "completed",
                 postcode_table: str = "postcode_table"):
        self.tables = {
            '{}'.format(postcode_table): ("CREATE TABLE `{}` ("
                                          "`ID` int(11) NOT NULL ,"
                                          "`country_code` varchar(20) NOT NULL, "
                                          "`postal_code` varchar(180) NOT NULL,"
                                          "`place_name` varchar(180) NOT NULL,"
                                          "`admin_name1` varchar(100) NOT NULL,"
                                          "`admin_code1` varchar(20) NOT NULL,"
                                          "`admin_name2` varchar(100) NOT NULL,"
                                          "`admin_code2` varchar(20) NOT NULL,"
                                          "`admin_name3` varchar(100) NOT NULL, "
                                          "`admin_code3` varchar(20) NOT NULL,"
                                          "`latitude` double NOT NULL,"
                                          "`longitude` double NOT NULL,"
                                          "`accuracy` varchar(11) NOT NULL"
                                          ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
                                          "ALTER TABLE `{}` ADD PRIMARY KEY (`ID`);"
                                          "ALTER TABLE `{}` MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;").format(
                postcode_table, postcode_table, postcode_table),
            '{}'.format(dictionary_table): ("CREATE TABLE `{}` (" +
                                            "`ID` int(11) NOT NULL," +
                                            "`Name` varchar(20) NOT NULL," +
                                            "`XLIDENTIFIER` varchar(100) NOT NULL" +
                                            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
                                            "ALTER TABLE `{}` ADD PRIMARY KEY (`ID`);"
                                            "ALTER TABLE `{}` MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;").format(
                dictionary_table, dictionary_table, dictionary_table),
            '{}'.format(completed_table): ("CREATE TABLE `{}` (" +
                                           "`ID` int(11) NOT NULL," +
                                           "`shipment_identcode` int(20) NOT NULL," +
                                           "`contract_type_id` int(100) NOT NULL," +
                                           "`shipment_createdate` datetime NOT NULL," +
                                           "`unix_shipment_createdate` DECIMAL(11,0) NOT NULL," +
                                           "`first_event` datetime NOT NULL," +
                                           "`unix_first_event` DECIMAL(11,0) NOT NULL," +
                                           "`last_event` datetime NOT NULL," +
                                           "`unix_last_event` DECIMAL(11,0) NOT NULL," +
                                           "`receiver_country_code` varchar(20) NOT NULL," +
                                           "`receiver_city_name` varchar(100) NOT NULL," +
                                           "`receiver_zip` varchar(20) NOT NULL," +
                                           "`receiver_latitude` double NOT NULL," +
                                           "`receiver_longitude` double NOT NULL," +
                                           "`sender_country_code` varchar(20) NOT NULL," +
                                           "`sender_city_name` varchar(100) NOT NULL," +
                                           "`sender_zip` varchar(20) NOT NULL," +
                                           "`sender_latitude` double NOT NULL," +
                                           "`sender_longitude` double NOT NULL," +
                                           "`distance` double NOT NULL" +
                                           ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
                                           "ALTER TABLE `{}` ADD PRIMARY KEY (`ID`);"
                                           "ALTER TABLE `{}` MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;").format(
                completed_table, completed_table, completed_table)}

        self.dbc = db_connector

    def __create_tables(self):

        for table_name in self.tables:
            cnx = self.dbc.create_Connection()
            cnx.database = self.dbc.database
            cursor = cnx.cursor()
            table_description = self.tables[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
            cursor.close()
            cnx.close()

    def __check_if_db_exist(self):
        db_name = self.dbc.database
        cnx = self.dbc.create_Connection()
        cursor = cnx.cursor()
        try:
            cursor.execute("USE {}".format(db_name))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(db_name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.__create_database(cursor, db_name)
                print("Database {} created successfully.".format(db_name))
                cnx.database = db_name
            else:
                print(err)
                exit(1)
        cnx.commit()
        cursor.close()
        cnx.close()

    @staticmethod
    def __create_database(cursor, db_name: str):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def initialize(self):
        self.__check_if_db_exist()
        self.__create_tables()

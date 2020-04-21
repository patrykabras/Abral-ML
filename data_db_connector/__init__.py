import mysql.connector
from mysql.connector import errorcode
import pandas as pd


class AbralDb:

    def __check_if_db_exist(self, user: str, db_name: str):
        cnx = mysql.connector.connect(user=user)
        cursor = cnx.cursor()
        try:
            cursor.execute("USE {}".format(db_name))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(db_name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(cursor, db_name)
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

    @staticmethod
    def __create_tables(config, db_name: str, TABLES):
        cnx = mysql.connector.connect(**config)
        cnx.database = db_name
        cursor = cnx.cursor()
        for table_name in TABLES:
            table_description = TABLES[table_name]
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

    @staticmethod
    def __fill_table(config, path: str, db_name: str, table_name: str, separator: str, rows: int):
        cnx = mysql.connector.connect(**config)
        cnx.database = db_name
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

    def load_data_into_base(self, db_name: str, table_name: str, path: str, rows=-1, separator="\t", user='root', password='',
                            host='127.0.0.1'):
        config = {
            'user': user,
            'password': password,
            'host': host,
            'raise_on_warnings': True
        }

        TABLES = {'{}'.format(table_name): ("CREATE TABLE `{}` ("
                                            "`ID` int(11) ,"
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
            table_name, table_name, table_name)}
        self.__check_if_db_exist(config.get('user'), db_name)
        self.__create_tables(config, db_name, TABLES)
        self.__fill_table(config, path, db_name, table_name, separator, rows)

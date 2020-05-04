import mysql.connector
from mysql.connector import errorcode


class DBConnector:

    def __init__(self, database_name: str = 'abraldb', user='root', password='', host='127.0.0.1'):
        self.config = {
            'user': user,
            'password': password,
            'host': host,
            'raise_on_warnings': True
        }
        self.database = database_name
        self.cnx = mysql.connector.connect(**self.config)
        # self.cnx.database = database_name
        mysql.connector.connect()

    def __del__(self):
        self.cnx.close()

    def create_Connection(self):
        return mysql.connector.connect(**self.config)

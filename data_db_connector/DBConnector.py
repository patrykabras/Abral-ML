import mysql.connector
from mysql.connector import pooling, errorcode


class DBConnector:

    def __init__(self, is_initial: bool = False, database_name: str = 'abraldb', user: str = 'root', password: str = '',
                 host: str = '127.0.0.1'):
        self.config = {
            'user': user,
            'password': password,
            'host': host,
            'raise_on_warnings': True
        }
        self.database = database_name
        if not is_initial:
            self.config['database'] = database_name

    def create_connection(self, pool_size: int) -> mysql.connector.connection:
        return pooling.MySQLConnectionPool(pool_name="basic-pool",
                                           pool_size=pool_size,
                                           **self.config)

    def create_single_connection(self) -> mysql.connector:
        return mysql.connector.connect(**self.config)

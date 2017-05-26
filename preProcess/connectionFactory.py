import MySQLdb


class MySqlConnector:

    connection = None
    cursor = None

    def __init__(self):
        pass

    def create_connection(self, host, user, passwd, db):
        MySqlConnector.connection = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
        return MySqlConnector.connection

    def close_connection(self):
        MySqlConnector.connection.close()

    def create_cursor(self):
        MySqlConnector.cursor = MySqlConnector.connection.cursor()

    def close_cursor(self):
        MySqlConnector.cursor.close()

    def get_result_by_query(self, query):
        MySqlConnector.cursor.execute(query)
        data = MySqlConnector.cursor.fetchall()
        return data

    def set_query(self, query):
        MySqlConnector.cursor.execute(query)

    def get_cursor(self):
        return MySqlConnector.cursor

    def get_connection(self):
        return MySqlConnector.connection
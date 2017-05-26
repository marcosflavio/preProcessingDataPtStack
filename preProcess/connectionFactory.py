import MySQLdb


class MySqlConnector:

    def __init__(self):
        self.connection = None
        self.cursor = None
        pass

    def create_connection(self, host, user, passwd, db):
        self.connection = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
        return self.connection

    def close_connection(self):
        self.connection.close()

    def create_cursor(self):
        self.cursor = self.connection.cursor()

    def close_cursor(self):
        self.cursor.close()

    def get_result_by_query(self, query):
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def set_query(self, query):
        self.cursor.execute(query)

    def get_cursor(self):
        return self.cursor

    def get_connection(self):
        return self.connection

from connectionFactory import MySqlConnector

mysql = MySqlConnector()

mysql.create_connection("localhost", "root", "root", "teste")
mysql.create_cursor()
mysql.set_query("delete from address where name_first = 'marcosfive'")

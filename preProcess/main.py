from connectionFactory import MySqlConnector

mysql = MySqlConnector()

mysql.create_connection("localhost", "root", "root", "teste")
mysql.create_cursor()
mysql.set_query("insert into address(name_first) values ('marcosfive')")
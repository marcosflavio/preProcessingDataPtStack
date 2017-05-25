import MySQLdb
import sys
connection = MySQLdb.connect(host = "localhost", user = "root", passwd = "root", db = "teste")
cursor = connection.cursor()
cursor.execute ("select name_first, name_last from address")
data = cursor.fetchall ()
cursor.close()
connection.close()
for row in data :
    print row[0], row[1]
sys.exit()
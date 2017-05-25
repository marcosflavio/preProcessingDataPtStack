import MySQLdb
import sys
connection = MySQLdb.connect(host = "localhost", user = "root", passwd = "root", db = "ptstack")
cursor = connection.cursor()
cursor.execute("SELECT VERSION()")
row = cursor.fetchone()
print "Versao do MySQL", row[0]
cursor.close()
connection.close()
sys.exit()
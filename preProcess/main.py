# -*- coding: latin-1 -*-

from connectionFactory import MySqlConnector
from portugueseProcess import TextCleaner
from preProcessingProcess import PreProcessing
mysql = MySqlConnector()

mysql.create_connection("localhost", "root", "root", "ptstack")
mysql.create_cursor()
data = mysql.get_result_by_query("select id , title from posts where post_type_id = 1")
mysql.close_connection()
mysql.close_cursor()

textCleaner = TextCleaner(False)
preProcess = PreProcessing(data, textCleaner)
preProcess.create_questions()

preProcess.remove_accent()
preProcess.remove_links()
preProcess.remove_rep_char()
preProcess.remove_symbols()
preProcess.remove_stop_words()
qs = preProcess.remove_sufix_portugues()

mysql.create_connection("localhost", "root", "root", "ptstack")
mysql.create_cursor()
cursor = mysql.get_cursor()
con = mysql.get_connection()
for q in qs:
    title = q.get_title()
    id = q.get_post_id()
    try:
        sql = "INSERT INTO questions (title, post_id) VALUES ('" + title + "'," + str(id) + ")"
        cursor.execute(sql)
        con.commit()
    except:
        con.rollback()
mysql.close_cursor()
mysql.close_connection()

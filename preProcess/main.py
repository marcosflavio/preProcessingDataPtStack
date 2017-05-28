# -*- coding: latin-1 -*-

from connectionFactory import MySqlConnector
from portugueseProcess import TextCleaner
from preProcessingProcess import PreProcessing
mysql = MySqlConnector()

mysql.create_connection("localhost", "root", "root", "ptstack")
mysql.create_cursor()
#mysql.set_query("insert into address(name_first) values ('MAÁÁÁÁÁÁRCOS')")
data = mysql.get_result_by_query("select id , title from posts where post_type_id = 1")
textCleaner = TextCleaner(False)
preProcess = PreProcessing(data, textCleaner)
preProcess.create_questions()

preProcess.remove_accent()
preProcess.remove_links()
qs = preProcess.remove_rep_char()
preProcess.remove_symbols()
preProcess.remove_stop_words()
preProcess.remove_sufix_portugues()

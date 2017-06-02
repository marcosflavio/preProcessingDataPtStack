# -*- coding: latin-1 -*-

from connectionFactory import MySqlConnector
from portugueseProcess import TextCleaner
from preProcessingProcess import PreProcessing
import unicodecsv as csv

header = ('title', 'post_id')

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

with open('/home/marcos/pt_stack_data/questionsPreProcess.csv', 'w') as f:
    writer = csv.writer(f, encoding='utf-8')
    writer.writerow(header)
    for q in qs:
        title = q.get_title()
        id = q.get_post_id()
        line = (title, id)
        writer.writerow(line)

import sys, time
import os, os.path
import mysql.connector
from mysql.connector import errorcode
from whoosh import index
from whoosh.index import create_in
from whoosh.fields import *

# directory to create index.
index_dir = "D:/bjstinfo_index"

# indexing the cursor fetched from database.
def db_indexer(cursor):
	if not os.path.exists(index_dir):
		os.mkdir(index_dir)
	schema = Schema(Title=NGRAMWORDS(stored=True), Url=ID(stored=True), Abstract=NGRAMWORDS(stored=True), Author=ID(stored=True), Keywords=KEYWORD(stored=True), Journal=ID(stored=True), Year_volumn=ID(stored=True))
	ix = create_in(index_dir, schema)
	writer = ix.writer()
	id = 0
	for (url, title, author, abstract, keywords, journal, year_volumn) in cursor:
		id += 1
		writer.add_document(Title=title, Url=url, Abstract=abstract, Author=author, Keywords=keywords, Journal=journal, Year_volumn=year_volumn)
	writer.commit()
	sys.stdout.write("\nindexing done!\n")

# database connection information
config = {
	'user': 'root',
	'password': 'root',
	'host': '10.108.224.39',
	'database': 'spider',
	'raise_on_warnings': True,
}

# retrieve data from remote mysql database, and indexing.
try:
	start_time = time.time()
	sys.stdout.write('connect to database\n')
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	sys.stdout.write('extract data from database\n')
	query = ("select url, title, author, abstract, keywords, journal, year_volumn from 2009_26;")
	cursor.execute(query)
	sys.stdout.write('indexing...')
	db_indexer(cursor)
	cursor.close()
	sys.stdout.write("time cost: " + str(time.time() - start_time) + " seconds\n")
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print "Something is wrong your username or password"
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print "Database does not exists"
	else:
		print err
else:
	cnx.close()

	


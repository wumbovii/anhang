#!/usr/bin/python
import MySQLdb
import json

SALARLY_FILES = ['salarly_managerjobs.json', 'salarly_pmjobs.json', 'salarly_softwarejobs.json',
'salarly_directorjobs.json', 'salarly_marketingjobs.json', 'salarly_salesjobs.json']

USERNAME = 'admin'
PASSWORD = 'password'
HOSTNAME = 'localhost'
DBNAME   = 'primsly'

def print_primslydb_info():
	# Open database connection
	db = MySQLdb.connect(HOSTNAME, USERNAME, PASSWORD, DBNAME)

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# execute SQL query using execute() method.
	cursor.execute('SELECT VERSION()')

	# Fetch a single row using fetchone() method.
	data = cursor.fetchone()

	print 'Database version : %s ' % data

	# disconnect from server
	db.close()

def create_tables():
	# Open database connection
	db = MySQLdb.connect(HOSTNAME, USERNAME, PASSWORD, DBNAME)

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# Drop table if it already exist using execute() method.
	cursor.execute('DROP TABLE IF EXISTS SALARLY')

	# Create table as per requirement
	sql = """CREATE TABLE SALARLY (
			 id INT AUTO_INCREMENT PRIMARY KEY,
	         city CHAR(28) NOT NULL,
	         company CHAR(52) NOT NULL,
	         title CHAR(52) NOT NULL,
	         state CHAR(2) NOT NULL,
	         salary INT NOT NULL)"""

	cursor.execute(sql)
	print('Executing command: ' + sql)
	# disconnect from server
	db.close()

def insert_into_salarly_table():
	# Open database connection
	db = MySQLdb.connect(HOSTNAME, USERNAME, PASSWORD, DBNAME)

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	#open json
	for f in SALARLY_FILES:
		json_data = open(f)
		print('reading ' + f + '...')
		data = json.load(json_data)

		for job in data:
			# Prepare SQL query to INSERT a record into the database.
			sql = "INSERT INTO SALARLY(city, company, title, state, salary) \
			         VALUES ('%s', '%s', '%s', '%s', '%d')" \
			         % (job['city'], job['company'], job['title'], job['state'], job['salary'])
			try:
			   # Execute the SQL command
			   cursor.execute(sql)
			   print('Executing command: ' + sql)
			   # Commit your changes in the database
			   db.commit()
			except:
			   # Rollback in case there is any error
			   print('SQL command fails: ' + sql)
			   db.rollback()

	# disconnect from server
	db.close()
#main
print_primslydb_info()
create_tables()
insert_into_salarly_table()
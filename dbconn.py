import pymysql
db = pymysql.connect("localhost","root","root","mydb",use_unicode=True, charset="utf8")
cursor = db.cursor()

def dbInitialize():
	query = "DROP TABLE IF EXISTS TWEETS1"
	cursor.execute(query)

	query = """CREATE TABLE TWEETS1 (
	PKTWEET VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL UNIQUE,
	TWEET TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
	POSITIVE FLOAT,
	NEGATIVE FLOAT,
	LOCATION VARCHAR(200),
	URL CHAR(100))CHARACTER SET utf8 COLLATE utf8_unicode_ci"""
	cursor.execute(query)

def dbInsertion(pk,tweet,pos,neg,url,location):
	query = "INSERT INTO TWEETS1 VALUES ('{}','{}',{},{},'{}','{}')".format(pk,tweet,pos,neg,location,url)
	#print(query)
	#cursor.execute(query)
	try:
   # Execute the SQL command
		cursor.execute(query)
   # Commit your changes in the database
		db.commit()
		#print("Committed")
	except Exception as e:
   # Rollback in case there is any error
		db.rollback()
		print("---Duplicate tweet detected! This tweet wont be written!")
		#print(str(e))
	
def dbClose():
	db.close()
	
def displayDB():
	query = "SELECT * FROM TWEETS1"
	data = cursor.execute(query)
	print(data)
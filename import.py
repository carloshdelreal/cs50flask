import csv, os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

##Set up the database
engine = create_engine("postgres://vkzngptialablm:4beecd9c16b5bd59a24b969e59878e2f8eed497625f029c0cab9854923b00932@ec2-23-21-65-173.compute-1.amazonaws.com:5432/dcde5js7tpbi42")
db = scoped_session(sessionmaker(bind=engine))

with open('books.csv', 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for idx,row in enumerate(spamreader):
	#isbn,title,author,year
		if idx == 0:
			print("Headers: "+str(row))
		else:	
			print(row)
			try:
				db.execute("INSERT INTO books ( isbn,title,author,year) VALUES (:isbn, :title, :author, :year )",
	                    { "isbn": row[0], "title": row[1].lower(), "author": row[2].lower(), "year": int(row[3]) } )
				db.commit()
			except:
				print("Something went wrong during copying the data to the database")
				break
    
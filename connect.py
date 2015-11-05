import sqlite3

path = '/Volumes/ExFat 1/database.sqlite'
conn = sqlite3.connect(path)
conn.row_factory = sqlite3.Row
c = conn.cursor()

data = c.execute('select author, count(*) from May2015 group by author order by count(*) desc limit 500').fetchall()
print data[0].keys()
for row in data:
	print row



# print c.execute('.tables')
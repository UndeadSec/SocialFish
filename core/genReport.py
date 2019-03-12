import sqlite3

def genReport(DATABASE, subject, user, company, date_range, target):
	conn = sqlite3.connect(DATABASE)
	cur = conn.cursor()	
	date_range = date_range.replace(' ', '')
	date_range = date_range.replace('/','-')
	date_range = date_range.split('_')
	date_start = date_range[0]
	date_end = date_range[1]
	sql = '''Select * from creds where pdate between '{}' and '{}' '''.format(date_start, date_end)
	results = cur.execute(sql).fetchall()
	print(results)
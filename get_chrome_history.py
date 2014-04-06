"""
Modified version of http://sumtxt.wordpress.com/2011/07/02/chrome-browser-history-in-r/
"""

import sqlite3
import codecs, re
 
pattern = "(((http)|(https))(www.))"

#Convert chrome webkit time to unix epoch 
SQL_STATEMENT = 'SELECT id, datetime((last_visit_time/1000000)-11644473600, \'unixepoch\', \'localtime\'), title, typed_Count, url, visit_count FROM urls WHERE (((last_visit_time/1000000) - 11644473600) > ( SELECT strftime(\'%s\',\'now\') - 108000));'
 
storage = codecs.open('out.csv', 'w', 'utf-8')
 

 
paths = ["/Users/divyanktk/Library/Application Support/Google/Chrome/Default/History"] 
 


def get_history():
	for path in paths:
		c = sqlite3.connect(path)
		for row in c.execute(SQL_STATEMENT):
			url = re.search(pattern, str(row[4]))
			try: urlc = url.group(0)
			except: urlc = "ERROR"
			if len(urlc) > 120:
				continue
			storage.write(str(row[0]) + "," + str(row[1]) + "," +'\"'+ str(row[2])+ '\"' + "," + str(row[3]) + "," + row[4] + "\n")
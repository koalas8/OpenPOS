#-*- encoding=utf-8 -*-

import psycopg2
from datetime import datetime
from datetime import timedelta

# 从当月开始，至第六个月的月份
tables = ['trans_' + t.strftime('%Y%m') for t in [datetime.now()+timedelta(days=d*31) for d in range(0, 6)]]

conn = psycopg2.connect('dbname=jf_card user=postgres password=123456')
cursor = conn.cursor()
for t in tables:
	try:
		cursor.execute("SELECT COUNT(*) cnt FROM pg_catalog.pg_class WHERE relname = %s", (t,))
		cnt = cursor.fetchone()[0]		
		if not cnt:			
			cursor.execute("CREATE TABLE %s () INHERITS (trans) WITH (OIDS=FALSE)" % t)		
			conn.commit()
			print "Creating table %s...success" % t
		else:
			print "Creating table %s...passed" % t
	except Exception, e:
		print e.message
		conn.rollback()
conn.close()			


import psycopg2
from collections import Counter

dbName = "censys"
table = "NL_DEVICES_ALL"
device = "nas"
ports = []

try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()

cur.execute("select * from nl_devices_all where metadata_device_type='nas'")
rows = cur.fetchall()
for row in rows:
	res = ""
	for r in row:
		res += str(r) + ","
	print res[0:len(res)-1]




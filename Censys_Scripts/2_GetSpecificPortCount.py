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

cur.execute("select ports from "+table+" where metadata_device_type='"+str(device)+"';")
rows = cur.fetchall()
for row in rows:
    ports.append(row[0])

ports = Counter(ports)
for port in ports:
  print str(port) + "," + str(ports[port])
import psycopg2

dbName = "censys"
table = "INDIA_DEVICES_ALL"
try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()

cur.execute("select metadata_device_type,count(metadata_device_type) count from "+table+" group by metadata_device_type order by count desc")
rows = cur.fetchall()
for row in rows:
    portsString = "["
    cur.execute("select ports from "+table+" where metadata_device_type='"+str(row[0])+"' group by ports")
    ports = cur.fetchall()
    for port in ports:
        portsString += str(port[0]) + ":"
    portsString = portsString[0:len(portsString)-1] + "]"
    print str(row[0])+","+str(portsString)+","+str(row[1])

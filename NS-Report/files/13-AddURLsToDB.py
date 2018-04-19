import psycopg2

dbName = "cowrie"

try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()

with open("urls.txt") as fp:
   url = fp.readline()
   while url:
       print url
       cur.execute("INSERT INTO MALICIOUS_URLS(URL) VALUES('" + str(url) + "')")
       conn.commit()
       url = fp.readline()

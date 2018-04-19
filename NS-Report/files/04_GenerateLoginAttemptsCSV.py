
import psycopg2

dbName = "cowrie"


try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()




cur.execute("SELECT LOGINATTEMPTS FROM STATS WHERE COUNTOFCOMMANDS = 0 ORDER BY LOGINATTEMPTS DESC")
rows = cur.fetchall()
print "Login_Attempts"
for row in rows:
   print(row[0])




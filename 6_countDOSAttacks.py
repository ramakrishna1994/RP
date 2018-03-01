import psycopg2

dbName = "cowrie"


cluster1center = 30.06456044
cluster2center = 10944.0
cluster3center = 17016.22222222

try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()

def selectCluster(dis1,dis2,dis3):
    if (dis1 < dis2) and (dis1 < dis3):
        return 1
    elif (dis2 < dis1) and (dis2 < dis3):
        return 2
    else:
        return 3


cur.execute("SELECT IP,LOGINATTEMPTS FROM STATS WHERE COUNTOFCOMMANDS = 0 ORDER BY LOGINATTEMPTS DESC")
rows = cur.fetchall()
for row in rows:
    clusterNo = selectCluster(abs(row[1]-cluster1center),abs(row[1]-cluster2center),abs(row[1]-cluster3center))
    cur.execute("UPDATE STATS SET DOSCLUSTER="+str(clusterNo)+" WHERE IP='"+str(row[0])+"';")
    conn.commit()

countOfSevereDosAttacks = 0
countOfMediumDosAttacks = 0
countOfLowDosAttacks = 0

cur.execute("SELECT COUNT(IP) FROM STATS WHERE DOSCLUSTER=1")
rows = cur.fetchall()
for row in rows:
    countOfLowDosAttacks = row[0]
    break

cur.execute("SELECT COUNT(IP) FROM STATS WHERE DOSCLUSTER=2")
rows = cur.fetchall()
for row in rows:
    countOfMediumDosAttacks = row[0]
    break

cur.execute("SELECT COUNT(IP) FROM STATS WHERE DOSCLUSTER=3")
rows = cur.fetchall()
for row in rows:
    countOfSevereDosAttacks = row[0]
    break

print "+++++----------------------------+"
print "++++| Severe DOS Attacks = "+str(countOfSevereDosAttacks)
print "++++| Medium DOS Attacks = "+str(countOfMediumDosAttacks)
print "++++| Low DOS Attacks    = "+str(countOfLowDosAttacks)
print "+++++----------------------------+"



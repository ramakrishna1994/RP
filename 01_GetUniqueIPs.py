import json
import requests
import psycopg2
from Globals import *


uniqueIPs = set()
dbName = "cowrie"

try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()

def createTables():
    cur.execute("CREATE TABLE IF NOT EXISTS STATS("
                "IP VARCHAR(20) PRIMARY KEY NOT NULL,"
                "LOGINATTEMPTS INT,"
                "COUNTOFCOMMANDS INT,"
                "DOSCLUSTER INT,"
                "SENTIMENT INT,"
                "COMMANDS TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS DOS_ATTACKS("
                "IP VARCHAR(20) PRIMARY KEY NOT NULL,"
                "LOGINATTEMPTS INT,"
                "COUNTOFCOMMANDS INT,"
                "COMMANDS TEXT)")

    conn.commit()
    cur.execute("TRUNCATE TABLE STATS")
    conn.commit()

createTables()


url = ELASTIC_URL + str("?size=1")
response = requests.get(url)
countOfData = json.loads(response.content)["hits"]["total"]
print countOfData

size = 10000

for i in range(0,countOfData+1,size):
    url = ELASTIC_URL + str("?_source=geoip.ip&size=")+str(size)+"&from="+str(i)
    response = requests.get(url)
    IPs = json.loads(response.content)["hits"]["hits"]
    print len(IPs)
    for IP in IPs:
        if IP["_source"] != {}:
            ip = IP["_source"]["geoip"]["ip"]
            uniqueIPs.add(ip)
    print "Completed : from = "+str(i)+" and end = "+str(i+size)

for ip in uniqueIPs:
    cur.execute("INSERT INTO STATS(IP) VALUES('"+ip+"')")
    conn.commit()

print "Total Number of Unique IP's = " + str(len(uniqueIPs))

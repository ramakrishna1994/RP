import json
import requests
import psycopg2
from Globals import *


dbName = "cowrie"
IPsArray = []

try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()

def getNoOfUniqueIPsFromDB():
    cur.execute("SELECT COUNT(*) FROM STATS");
    rows = cur.fetchall()
    for row in rows:
        return row[0]

def getIPsFromDB():
    cur.execute("SELECT IP FROM STATS");
    rows = cur.fetchall()
    for row in rows:
        IPsArray.append(row[0])


print getNoOfUniqueIPsFromDB()
getIPsFromDB()

for i in range(0,getNoOfUniqueIPsFromDB()):
    tillNowCommandsExecuted = ""
    data = {
       "query": {
            "query_string" : {
                "fields" : ["src_ip","eventid"],
                "query"  : str(IPsArray[i])+" AND cowrie.login.*"
            }
        },
        "_source": ["geoip.ip","eventid","message"]
    }
    headers = {"Content-Type": "application/json"}
    url = ELASTIC_URL + str("?size=1")
    response = requests.post(url,data=json.dumps(data),headers=headers)
    noOfLoginAttempts = json.loads(response.content)["hits"]["total"]
    cur.execute("UPDATE STATS SET LOGINATTEMPTS=" + str(noOfLoginAttempts) + "WHERE IP='" + IPsArray[i] + "';")
    conn.commit()

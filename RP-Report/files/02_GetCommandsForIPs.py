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
                "query" : ""+str(IPsArray[i])+" AND cowrie.command.input"
            }
        },
        "_source": ["geoip.ip","eventid","message"]
    }
    headers = {"Content-Type": "application/json"}
    url = ELASTIC_URL + str("?size=10000")
    response = requests.post(url,data=json.dumps(data),headers=headers)
    countOfCommands = json.loads(response.content)["hits"]["total"]
    cur.execute("UPDATE STATS SET COUNTOFCOMMANDS=" + str(countOfCommands) + "WHERE IP='" + IPsArray[i] + "';")
    conn.commit()
    commands = json.loads(response.content)["hits"]["hits"]
    if commands != []:
        for command in commands:
            tillNowCommandsExecuted += str(command["_source"]["message"].replace("CMD:","")) + " "
        print tillNowCommandsExecuted
    cur.execute("UPDATE STATS SET COMMANDS='" + str(tillNowCommandsExecuted.replace("'","").strip()) + "' WHERE IP='" + IPsArray[i] + "';")
    conn.commit()

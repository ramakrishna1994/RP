import requests
import psycopg2
from collections import Counter
import json

dbName = "cowrie"
apikey = "f0aa0772e518487aa5daf1dcf2be2d37c9b9b361b1a0d8339faf972210b36d41"
offset = 1


def getScanResults(scan_id):
    softwares = ""
    report_url = 'https://www.virustotal.com/vtapi/v2/url/report?' \
                 'apikey=' + str(apikey) + '&' \
                 'resource=' + str(scan_id) + '&' \
                 'allinfo=false'

    response = requests.get(report_url)
    res = response.json()
    #print json.dumps(res['scans'], indent=4, sort_keys=True)
    for r in res['scans']:
        if res['scans'][r]['detected'] == True:
            softwares += str(r) + ";"
    print scan_id
    print softwares
    softwares = softwares[0:len(softwares)-1]
    positives = res['positives']
    total = res['total']
    cur.execute("UPDATE MALICIOUS_URLS SET POSITIVES="+str(positives)+", TOTAL="+str(total)+" ,IDENTIFIED_ENGINES='"+str(softwares)+"';")
    conn.commit()



try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()

cur.execute("SELECT SCAN_URL FROM MALICIOUS_URLS OFFSET "+str(offset))
scan_ids = cur.fetchall()
i = offset
for id in scan_ids:
    print "**********************************************************"
    print i
    i = i+1
    getScanResults(id[0])


import requests
import json
import psycopg2

apikey = "f0aa0772e518487aa5daf1dcf2be2d37c9b9b361b1a0d8339faf972210b36d41"
scan_url = 'https://www.virustotal.com/vtapi/v2/ip-address/report?apikey='+apikey+'&ip='
uniqueURLs = set()

dbName = "cowrie"
offset = 1813
try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()

#cur.execute("CREATE TABLE IF NOT EXISTS MALICIOUS_URLS(URL TEXT)")
#cur.execute("TRUNCATE TABLE MALICIOUS_URLS")
#conn.commit()

cur.execute("SELECT IP FROM STATS OFFSET "+str(offset));
rows = cur.fetchall()
i = offset
for row in rows:
    print "**********************************"
    print i
    i += 1
    print row[0]
    r = requests.get(str(scan_url)+str(row[0]))
    resp = json.loads(r.content)
    #print resp
    if "detected_urls" in resp:
        if resp["detected_urls"] != []:
            #print resp["detected_urls"]
            for url in resp["detected_urls"]:
                print url["url"]
                cur.execute("INSERT INTO MALICIOUS_URLS(URL) VALUES('" + url["url"] + "')")
                conn.commit()




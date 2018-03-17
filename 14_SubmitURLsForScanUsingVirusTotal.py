import json
import psycopg2
from subprocess import check_output

dbName = "cowrie"
apikey = "f0aa0772e518487aa5daf1dcf2be2d37c9b9b361b1a0d8339faf972210b36d41"
scan_url = 'https://www.virustotal.com/vtapi/v2/url/scan'

offset = 805

try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()


cur.execute("SELECT URL FROM MALICIOUS_URLS ORDER BY URL OFFSET "+str(offset))
urls = cur.fetchall()
i=offset
for url in urls:
    print "**************************************************"
    print i
    i += 1
    res = json.loads(check_output(["curl", "--request", "POST",
                                  "--url", "https://www.virustotal.com/vtapi/v2/url/scan",
                                  "--data", "apikey=" + apikey,
                                  "--data", "url=" + url[0]]))
    print res['scan_id']
    cur.execute("UPDATE MALICIOUS_URLS SET SCAN_URL='"+str(res['scan_id'])+"' WHERE URL='"+str(url[0])+"';")
    conn.commit()








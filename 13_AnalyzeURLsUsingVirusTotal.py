import requests
import json
from subprocess import check_output
from collections import Counter

apikey = "f0aa0772e518487aa5daf1dcf2be2d37c9b9b361b1a0d8339faf972210b36d41"
scan_url = 'https://www.virustotal.com/vtapi/v2/url/scan'
scan_ids = []
softwares = []

def getScanResults(scan_id):
    report_url = 'https://www.virustotal.com/vtapi/v2/url/report?' \
                 'apikey=' + apikey + '&' \
                 'resource=' + scan_id + '&' \
                 'allinfo=false'

    response = requests.get(report_url)
    res = response.json()
    #print json.dumps(res['scans'], indent=4, sort_keys=True)
    print res['url']
    print res['positives']
    print "----------------"
    for r in res['scans']:
        if res['scans'][r]['detected'] == True:
            print str(r) + "_____|____" + str(res['scans'][r]['detected']) + "_____|____" + str(res['scans'][r]['result'])
            softwares.append(r)

with open("urls.txt") as fp:
   url = fp.readline()
   while url:
       print url
       res = json.loads(check_output(["curl", "--request", "POST",
                                      "--url", "https://www.virustotal.com/vtapi/v2/url/scan",
                                      "--data", "apikey=" + apikey,
                                      "--data", "url=" + url]))
       print res['scan_id']
       scan_ids.append(res['scan_id'])
       url = fp.readline()

for id in scan_ids:
    print "**********************************************************"
    getScanResults(id)

print "*************************************************************"
print Counter(softwares)






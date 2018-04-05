import psycopg2
from collections import Counter
from prettytable import PrettyTable
from termcolor import colored
import sys

IdentifiedEnginesCount = PrettyTable(['Antivirus Engine', 'Identified Count'])
MaliciousURLSCount = PrettyTable(['URL', 'Positives','Total'])

uniqueURLs = set()
dbName = "cowrie"
#ipToTest = "192.200.218.166"
#print str(sys.argv)
ipToTest = str((sys.argv)[1])
engines = []
malicious = 0;

try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()

cur.execute("SELECT URL,POSITIVES,TOTAL,IDENTIFIED_ENGINES FROM MALICIOUS_URLS WHERE URL LIKE '%"+str(ipToTest)+"%'")
rows = cur.fetchall()
for row in rows:
    for engine in row[3].split(";"):
        malicious = 1
        engines.append(engine)
        if row[0]!="":
            uniqueURLs.add(row[0].strip())


for url in uniqueURLs:
    cur.execute("SELECT URL,POSITIVES,TOTAL FROM MALICIOUS_URLS WHERE URL LIKE '%"+str(url)+"%' LIMIT 1")
    rows = cur.fetchall()
    for row in rows:
        MaliciousURLSCount.add_row([row[0].strip(),row[1],row[2]])

if(malicious == 1):
    print "+---------------------------------------------------------+"
    print "| IP : "+str(ipToTest) + " is Classified as "+colored('Malicious', 'red',attrs=['bold'])+"         |";
    print "+---------------------------------------------------------+"

    print "+---------------------------------------------------------+"
    print "| Identified as "+colored('Malicious', 'red',attrs=['bold'])+" By Below Antivirus Engines      |"
    print "+---------------------------------------------------------+"
    counts = Counter(engines)
    for engine in counts:
        IdentifiedEnginesCount.add_row([engine,counts.get(engine)])

    print IdentifiedEnginesCount
    print "+----------------------------------------------------------------------+"
    print "|    Identified Below URLs as Malicious pertaining to the given IP     |"
    print "+----------------------------------------------------------------------+"

    print MaliciousURLSCount

else:
    print "+---------------------------------------------------------+"
    print "|   No Data Found in the Database for the Specified IP    |"
    print "|   IP : " + str(ipToTest) + " is "+colored('Not Malicious', 'green',attrs=['bold'])+"                 |";
    print "+---------------------------------------------------------+"

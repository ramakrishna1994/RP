import psycopg2
import re

dbName = "cowrie"
totalWords = []
uniqueWords = set()
probabilities = {}
sentiments = []
urls = []
uniqueBinaries = set()
strippedBinaries = set()
uniqueURLs = set()

try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()

cur.execute("SELECT COMMANDS FROM STATS")
rows = cur.fetchall()
for row in rows:
    commands = row[0].replace(";"," ").split(" ")
    for command in commands:
        if command != "":
            uniqueWords.add(command.strip())
            totalWords.append(command.strip())

for i in range(0,len(totalWords)):
    if totalWords[i] == "wget":
        if totalWords[i+1] != "":
            urls.append(totalWords[i+1])



cur.execute("SELECT IP,COMMANDS FROM STATS")
rows = cur.fetchall()
for row in rows:
    commands = row[1].replace(";"," ").split(" ")
    for command in commands:
        if command != "":
            if re.match('./([a-z]|[A-Z]|[0-9])+', command):
                uniqueBinaries.add(command)

for binary in uniqueBinaries:
    strippedBinaries.add(binary[2:len(binary)])


print "=============="

for word in totalWords:
    for binary in strippedBinaries:
        if "http" in word:
            uniqueURLs.add(word.replace("\n"," ").split(" ")[0])

for url in uniqueURLs:
    print(url)

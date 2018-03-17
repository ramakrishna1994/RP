import psycopg2
from collections import Counter
import math

dbName = "cowrie"
totalWords = []
uniqueWords = set()
probabilities = {}
sentiments = []

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

counts = Counter(totalWords)
for word in uniqueWords:
    probability = (float)(counts.get(word) + 1) / (float)(len(totalWords) + len(uniqueWords))
    probabilities.setdefault(word,math.exp(probability))


cur.execute("SELECT IP,COMMANDS FROM STATS")
rows = cur.fetchall()
for row in rows:
    TotalProb = 1.0
    commands = row[1].replace(";"," ").split(" ")
    for command in commands:
        if command != "":
            if probabilities.get(command) != None:
                TotalProb *= probabilities.get(command)
    #print str(row[0]) + "=================>" + str(TotalProb)
    if TotalProb != 1.0:
        sentiments.append((row[0],TotalProb))

print "Sentiments"
for sentiment in sentiments:
    print sentiment[1]



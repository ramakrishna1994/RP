import psycopg2
from collections import Counter
import math

dbName = "cowrie"
totalWords = []
uniqueWords = set()
probabilities = {}
sentiments = []
classification = []
center_1 =  1.65478756
center_2 = 2.87508731e+08
class_1=0
class_2=0
class_3=0

def classify(dis):
    dis1 = abs(center_1 - dis)
    dis2 = abs(center_2 - dis)
    if dis2 > dis1:
        return 2
    else:
        return 3


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
    sentiments.append((row[0],TotalProb))

for sentiment in sentiments:
    if sentiment[1] == 1.0:
        classification.append((sentiment[0],sentiment[1],1))
    else:
        classification.append((sentiment[0],sentiment[1],classify(sentiment[1])))

for clasif in classification:
    print str(clasif[0])+"========="+str(clasif[1])+str("==========")+str(clasif[2])
    if clasif[2] == 1:
        class_1 += 1
    elif clasif[2] == 2:
        class_2 += 1
    else:
        class_3 += 1


print "+++++------- No Of IPs ----------+"
print "++++| Critical = "+str(class_3)
print "++++| Medium   = "+str(class_2)
print "++++| Low      = "+str(class_1)
print "+++++----------------------------+"



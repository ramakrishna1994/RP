import psycopg2
import re

#pattern = re.compile("^([A-Z][0-9]+)+$")

#re.match('./([a-z]|[A-Z]|[0-9])+', './123asdf')


dbName = "cowrie"
totalWords = []
uniqueBinaries = set()



try:
    conn = psycopg2.connect("dbname='"+str(dbName)+"' user='postgres' host='localhost' password='postgres'")
except Exception as e:
    print e
cur = conn.cursor()

cur.execute("SELECT IP,COMMANDS FROM STATS")
rows = cur.fetchall()
for row in rows:
    commands = row[1].replace(";"," ").split(" ")
    for command in commands:
        if command != "":
            if re.match('./([a-z]|[A-Z]|[0-9])+', command):
                uniqueBinaries.add(command)
                print(str(row[0])+" ==========> "+str(command))

print "+-----------------------+"
print "+        Binaries       +"
print "+-----------------------+"
for binary in uniqueBinaries:
    print binary
print "+-----------------------+"
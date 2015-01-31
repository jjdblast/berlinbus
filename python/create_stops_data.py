import json
import sqlite3

con = sqlite3.connect('vbb.db')
con.text_factory = str
cur = con.cursor()

# initialize the dictionary
bla = { 'stops': [] }

# ID, NAME, LAT, LON
for c in cur.execute("SELECT DISTINCT * FROM stops"):
    bla['stops'].append([c[0], c[1], c[2], c[3]])

con.close

with open('../webdata/stops.txt', 'w') as outfile:
    json.dump(bla, outfile)

print 'done. beautiful :)\n'

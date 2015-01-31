import json
import sqlite3
import collections

con = sqlite3.connect('vbb.db')
con.text_factory = str
cur = con.cursor()

# grab all routes
cur.execute("SELECT DISTINCT route_id, route_short_name from routes")
lines = cur.fetchall()

# initialize the dictionary
bla = { }

for l in lines:

    # only process the trip of this line that has the highest frequency
    cur.execute("SELECT DISTINCT trip_id FROM trips_unique WHERE route_id={0} AND trip_frequency=(SELECT MAX(trip_frequency) from trips_unique WHERE route_id={0})".format(l[0]))
    trips = cur.fetchall()

    bla[l[1]] = [1]
    for t in trips:
    	bla[l[1]][0] = []
        for c in cur.execute("SELECT stop_lat, stop_lon FROM lookup WHERE trip_id=%s" % t):
            bla[l[1]][0].append(c[0]);
            bla[l[1]][0].append(c[1]);

con.close

with open('../webdata/routes.txt', 'w') as outfile:
    json.dump(bla, outfile)

print 'done. beautiful :)\n'

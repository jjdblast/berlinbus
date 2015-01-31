

import csv
import sqlite3

con = sqlite3.connect('vbb.db')
con.text_factory = str
cur = con.cursor()

# debug out all
cur.execute("SELECT DISTINCT route_id, route_short_name from routes")
lines = cur.fetchall()

#trips = cur.execute("SELECT DISTINCT trip_id from lookup where route_short_name='104'")
#for t in trips
#    print t


#for row in lines:
#    print ''.join(row)

with open('final_data.txt', 'wb') as f:
    print >> f, '{'

    for l in lines:
        print >> f, '"', ''.join(l[1]), '": [',

        cur.execute("SELECT DISTINCT trip_id FROM lookup WHERE route_id={0} AND trip_frequency=(SELECT MAX(trip_frequency) from lookup WHERE route_id={0})".format(l[0]))
        trips = cur.fetchall()

        for t in trips:
            #print 'trip: ', t
            print >> f, '[',
            data = cur.execute("SELECT DISTINCT stop_coordinates FROM lookup WHERE trip_id=%s" % t)

            for row in data:
                print >> f, ''.join(row), ',',
            print >> f, '], '


        print >> f, '], '

    print >> f, '}'

con.close


#with open('final_data.txt', 'rb') as f:
#    print ''.join(f)

print 'done. beautiful :)\n'

#with open ('test.csv', 'rb') as f:
#	reader = csv.reader(f)
#	for row in reader:
#		print row
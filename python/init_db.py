import csv
import sqlite3

con = sqlite3.connect('vbb.db')
#con = sqlite3.connect(':memory:')
con.text_factory = str
cur = con.cursor()

################
### READ STOPS [bus stop names & locations]
# stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station
cur.execute("DROP TABLE IF EXISTS stops;")
cur.execute("CREATE TABLE stops (stop_id integer primary key,stop_name text,stop_coordinates text);")

with open ('data/stops.txt', 'rb') as f:
	# csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(f) # comma is default delimiter
    to_db = [(i['stop_id'], i['stop_name'], i['stop_lat'] +','+ i['stop_lon']) for i in dr]

cur.executemany("INSERT INTO stops (stop_id,stop_name,stop_coordinates) VALUES (?, ?, ?);", to_db)

################
### READ ROUTES [bus line names]
# route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color
cur.execute("DROP TABLE IF EXISTS routes;")
cur.execute("CREATE TABLE routes (route_id integer primary key,route_short_name text);")

with open ('data/routes.txt', 'rb') as f:
	# csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(f) # comma is default delimiter
    to_db = [(i['route_id'], i['route_short_name']) for i in dr]

cur.executemany("INSERT INTO routes (route_id,route_short_name) VALUES (?, ?);", to_db)

################
### READ TRIPS
# route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,block_id,shape_id
cur.execute("DROP TABLE IF EXISTS trips;")
cur.execute("CREATE TABLE trips (trip_id integer primary key, route_id integer);")

with open ('data/trips.txt', 'rb') as f:
	# csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(f) # comma is default delimiter
    to_db = [(i['trip_id'], i['route_id']) for i in dr]

cur.executemany("INSERT INTO trips (trip_id, route_id) VALUES (?, ?);", to_db)

################
### READ STOP_TIMES
# trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled
cur.execute("DROP TABLE IF EXISTS stop_times;")
cur.execute("CREATE TABLE stop_times (trip_id integer,stop_id integer);")

with open ('data/stop_times.txt', 'rb') as f:
	# csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(f) # comma is default delimiter
    to_db = [(i['trip_id'], i['stop_id']) for i in dr]

cur.executemany("INSERT INTO stop_times (trip_id,stop_id) VALUES (?, ?);", to_db)

### commit all to the DB
con.commit()

con.close

print 'database initialized'

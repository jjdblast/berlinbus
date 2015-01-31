import sqlite3

con = sqlite3.connect('vbb.db')
con.text_factory = str
cur = con.cursor()

# create a temp table to remove duplicate trips that contain the exact same stops
# to do so, we generate a hashtag that represents one complete trip
cur.execute("DROP TABLE IF EXISTS temp;")
cur.execute("CREATE TABLE temp (trip_id integer, route_id integer, hashtag integer);");
data = cur.execute("INSERT INTO temp SELECT DISTINCT trips.trip_id, routes.route_id, SUM(stop_id) "
   "FROM trips, stop_times, routes "
   # "WHERE trips.route_id=224 "
   "WHERE routes.route_id=trips.route_id "
   "AND trips.trip_id=stop_times.trip_id "
   "GROUP BY trips.trip_id")

# create a new trips table that only contains unqiue trips and their frequency
cur.execute("DROP TABLE IF EXISTS trips_unique;")
data = cur.execute("CREATE TABLE trips_unique AS SELECT trip_id, route_id, COUNT(hashtag) as trip_frequency "
   "FROM temp "
   "GROUP BY hashtag")

# clean up temp table
cur.execute("DROP TABLE IF EXISTS temp;")

# create a denormalized lookup table containing all data we need
cur.execute("DROP TABLE IF EXISTS lookup;")
cur.execute("CREATE TABLE lookup AS SELECT DISTINCT stop_times.trip_id, routes.route_id, route_short_name, stop_name, stop_lat, stop_lon, trip_frequency "
            "FROM stop_times, stops, trips_unique, routes "
            "WHERE stop_times.trip_id = trips_unique.trip_id "
            "AND stop_times.stop_id = stops.stop_id "
            "AND trips_unique.route_id = routes.route_id"
            )

con.commit()
con.close

print 'done. beautiful :)\n'
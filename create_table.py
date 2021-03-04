import sqlite3

conn = sqlite3.connect('geolocation_info.db')
conn.execute('DROP TABLE IF EXISTS GeolocationInfo ')
conn.execute('CREATE TABLE GeolocationInfo (ip TEXT PRIMARY KEY, continent_name TEXT, country_name TEXT, latitude TEXT, longitude TEXT, zip TEXT)')
conn.close()
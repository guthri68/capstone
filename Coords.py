from skyfield import api
from skyfield.api import load
from skyfield import almanac
from datetime import timedelta
import mysql.connector
from mysql.connector import errorcode

# Adjust database connection here
DB_NAME = 'astronomy_app'
DB_HOST = '127.0.0.1'
DB_USER = 'node'
DB_PASS = 'node'


# Attempt to connect to database
try:
    db = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
    cursor = db.cursor()
    print("Successfully connected to database")
except mysql.connector.Error as err:
    print("Something went wrong with connecting to the database:")
    print(err)

# Attempt to create table for rise and set times of various objects
try:
    print("Creating rise_set table")
    cursor.execute(
    """
    CREATE TABLE if not exists `rise_set`
    (
      `ID` int(4) NOT NULL AUTO_INCREMENT,
      `OBJECT_NAME` varchar(45) NOT NULL,
      `RISE` varchar(30) NOT NULL,
      `SET` varchar(30) NOT NULL,
      PRIMARY KEY (`ID`)
    ) ENGINE=InnoDB
    """)
    print("Successfully created rise_set table")
except mysql.connector.Error as err:
    print("Something went wrong with creating the rise_set table")
    print(err)

add_rise_set = ("""
INSERT INTO rise_set
VALUES (%s, %s, %s, %s)
""")

eph = load('de421.bsp')
p_names = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
p_codes = [1, 2, 4, 5, 6, 7, 8]
ts = api.load.timescale()
t0 = ts.now()
t1 = ts.utc(t0.utc_datetime() + timedelta(days=1))
location = api.wgs84.latlon(39.700096, -75.111423) # Glassboro, NJ

for code, planet in zip(p_codes, p_names):
    f = almanac.risings_and_settings(eph, eph[code], location)
    t, y = almanac.find_discrete(t0, t1, f)
    
    for ti, yi in zip(t, y):
        if yi:
            rise_t = ti.utc_iso()
        else:
            set_t = ti.utc_iso()
    insert = (code, planet, rise_t, set_t)
    cursor.execute(add_rise_set, insert)
db.commit()
print("Successfully inserted rise and set times of the planets")
cursor.close()
db.close()

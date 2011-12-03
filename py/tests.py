#tests.py - Some tests for our awesome app

from pysqlite2 import dbapi2 as sqlite3
import random
import datetime

#Docs for pysqlite: http://pysqlite.googlecode.com/svn/doc/sqlite3.html

create_statement = """
    CREATE TABLE ClimateGrid (
        Row INT NOT NULL,
        Col INT NOT NULL,
        Precip FLOAT,
        Min_T FLOAT,
        Max_T FLOAT,
        Seq INT NOT NULL,
        Year INT NOT NULL,
        Month INT NOT NULL,
        Day INT NOT NULL)"""

insert_statement = """
    INSERT INTO ClimateGrid (Row, Col, Precip, Min_T, Max_T, Seq, Year, Month, Day)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

class ClimateGridInterface:
    """
    Defines some interface methods for our ClimateGrid table
    Work in progress, do not use as is.
    """

    nrows = 360
    ncols = 720

    def round_to_nearest_half(x):
        return round(2 * x) / 2

    @staticmethod
    def latlng_to_rowcol(lat, lng):
        """
        Given latitude and longitude returns (row, col) for grid 
        or None if out of bounds
        """
        if lat < -90 or lat > 90 or lng < -180 or lng > 180:
            return None
        lat = self.round_to_nearest_half(lat)
        lng = self.round_to_nearest_half(lng)
        row = (lat + 90) * nrows / 180
        col = (lng + 180) * ncols / 360
        row = int(row) % nrows
        col = int(col) % ncols
        return (row, col)

        

class Helper:
    @staticmethod
    def index_to_sequence(row, col):
        """
        Converts a (row, col) index to a sequence number
        """
        return col * 720 + row

    @staticmethod
    def rand_temp():
        """Returns a random temperature 
        """
        return random.randint(-30, 110) + random.random();

    @staticmethod
    def offset_to_month_day(year, offset):
        """
        Given a year and a number of days offset, returns a tuple
        (month, day) for the date of first day of year
         + offset
        """
        start = datetime.datetime(year, 1, 1)
        offset = datetime.timedelta(offset)
        end = start + offset
        return (end.month, end.day)

#Let's see if we can make a db and get some stuff out of it

#connect can take a file path for a db file, or ':memory:' to create a db in RAM
dbfile = 'test.sqlite'
conn = sqlite3.connect(dbfile)
c = conn.cursor()
c.execute(create_statement)

year = 1998

#Ok, this is way too big, let's make it a bit smaller
#for doy in xrange(1, 366):
#for doy in xrange(1, 30):
for doy in xrange(1, 2):
    print("Adding day " + str(doy) + "...")
    for row in xrange(0, 720):
        for col in xrange(0, 360):
            seq = Helper.index_to_sequence(row, col)
            min_temp = Helper.rand_temp()
            max_temp = Helper.rand_temp()
            if max_temp < min_temp:
                t = max_temp
                max_temp = min_temp
                min_temp = t

            precip = 5 * random.random()
            md = Helper.offset_to_month_day(year, doy)
            month = md[0]
            day = md[1]
            insert_data = (row, col, precip, min_temp, max_temp, seq, year, month, day)
            c.execute(insert_statement, insert_data)

conn.commit()
conn.close()

#Make sure it's still there...
conn = sqlite3.connect(dbfile)
c = conn.cursor()

print(c.execute("SELECT * FROM ClimateGrid WHERE Row = 80 AND Col = 135").fetchall())

conn.close()



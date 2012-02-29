#Defines an interface to our database
# -*- coding: utf-8 -*-

from pysqlite2 import dbapi2 as sqlite3
import datetime
import pdb

class ClimateGridInterface(object):
    """
    Defines some interface methods for our ClimateGrid table
    Automatically connects to the db upon creation and creates the necessary tables
    """

    conn = None      #db connection
    curs = None      #cursor for connection

    def __init__(self, dbname="./py/testdb.sqlite"):
        #Docs for pysqlite: http://pysqlite.googlecode.com/svn/doc/sqlite3.html
        self.conn = sqlite3.connect(dbname)
        self.conn.isolation_level = "DEFERRED"
        self.curs = self.conn.cursor()
        try:
            self.curs.execute(self._create_statement)
            print("Successfully created new database!")
        except sqlite3.OperationalError:
            # table already exists, we don't need to do anything
            pass

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    _nrows = 360
    _ncols = 720

    _create_statement = """
    CREATE TABLE ClimateGrid (
            Row INT2 NOT NULL,
            Col INT2 NOT NULL,
            Precip FLOAT4,
            Min_T FLOAT4,
            Max_T FLOAT4,
            Seq INT NOT NULL,
            Date VARCHAR(8) COLLATE BINARY)
    """
        #Year INT NOT NULL,
        #Month INT NOT NULL,
        #Day INT NOT NULL)"""

    _insert_statement = """
            INSERT INTO ClimateGrid (Row, Col, Precip, Min_T, Max_T, Seq, Date)
            VALUES (?, ?, ?, ?, ?, ?, ?)"""

    _get_rows_by_xy_sql = """
            SELECT Precip, Min_T, Max_T, Date FROM ClimateGrid
                    WHERE Row = ? AND Col = ?
                    ORDER BY Date
            """

    def round_to_nearest_half(self, x):
        return round(2 * x) / 2

    def latlng_to_rowcol(self, lat, lng):
        """
        Given latitude and longitude returns (row, col) for grid
        or None if out of bounds
        """
        if lat < -90 or lat > 90 or lng < -180 or lng > 180:
            return None
        lat = self.round_to_nearest_half(lat)
        lng = self.round_to_nearest_half(lng)
        row = (90 - lat) * self._nrows / 180
        col = (lng + 360) * self._ncols / 360
        row = int(row) % self._nrows
        col = int(col) % self._ncols
        row = self._nrows - row;
        print (row, col)
        return (row, col)

    def index_to_sequence(self, row, col):
        """
        Converts a (row, col) index to a sequence number
        """
        return row * self._ncols + col

    def import_files(self, f_precip, f_mint, f_maxt, year, month, day, doy):
        """
        Imports one day's worth of information
        year, month, day are all 1 based
        @param f_precip: file data for precipiation (one dimensional array of floats)
        @param f_mint: file data for min temperature (one dimensional array of floats)
        @param f_maxt: file data for max temperature  (one dimensional array of floats)
        @param year: year of the data we're importing
        @param month: month of the data we're importing
        @param day: day of the data we're importing
        @param doy: day of year of the data we're importing (1 - 366)
        """
        for i in xrange(len(f_precip)):
            row, col = int(i / self._ncols), i % self._ncols
            precip = f_precip[i]
            min_temp = f_mint[i]
            max_temp = f_maxt[i]
            if precip == -999: precip = None
            if min_temp == -999: min_temp = None
            if max_temp == -999: max_temp = None
            if precip is None and min_temp is None and max_temp is None:
                continue

            date = str("%04d%02d%02d" % (year, month, day))
            insert_data = (row, col, precip, min_temp, max_temp, i, date)
            self.insert_row(insert_data)

    def insert_row(self, data):
        self.curs.execute(self._insert_statement, data)

    def get_row_by_xy(self, data):
        """
        Gets all entries for a given location
        @param data:dictionary with x and y in degrees
        @returns: an array of rows, or [] if none are found
        Row values are [Precip, Min_T, Max_T, Date]
        """
        #Uncomment this when this is done
        #print(data)
        lat = data['y']
        lng = data['x']
        result = []
        params = self.latlng_to_rowcol(lng, lat)

        if params is not None:
            #print(params)
            rows = self.curs.execute(self._get_rows_by_xy_sql, params)
            result = rows.fetchall()
            #print(result)
            #result = (10, 44, 0.0, 3.265, 8.458, 364, 2006, 12, 30)

        return result

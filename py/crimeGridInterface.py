#Defines an interface to our database

from pysqlite2 import dbapi2 as sqlite3
import datetime

class ClimateGridInterface:
    """
    Defines some interface methods for our ClimateGrid table
    Automatically connects to the db upon creation and creates the necessary tables
    """

    conn = None     #db connection
    curs = None     #cursor for connection

    def __init__():
        conn = sqlite3.connect("./crimegrid.sqlite")
        c = conn.cursor()
        #TODO: test for existence of our db, create only if necessary
        c.execute(self._create_statement)

    _nrows = 360
    _ncols = 720

    _create_statement = """
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

    _insert_statement = """
        INSERT INTO ClimateGrid (Row, Col, Precip, Min_T, Max_T, Seq, Year, Month, Day)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    def round_to_nearest_half(x):
        return round(2 * x) / 2

    def latlng_to_rowcol(lat, lng):
        """
        Given latitude and longitude returns (row, col) for grid 
        or None if out of bounds
        """
        if lat < -90 or lat > 90 or lng < -180 or lng > 180:
            return None
        lat = self.round_to_nearest_half(lat)
        lng = self.round_to_nearest_half(lng)
        row = (lat + 90) * _nrows / 180
        col = (lng + 180) * _ncols / 360
        row = int(row) % _nrows
        col = int(col) % _ncols
        return (row, col)

    def index_to_sequence(row, col):
        """
        Converts a (row, col) index to a sequence number
        """
        return col * 720 + row

	def import_files(fa, fb, fc, year, month, day, doy, c):
		for i in xrange(len(fa)):
			if -999 in (fa[i],fb[i],fc[i]):
				continue
			row, col = int(i/360),i%720
			precip = None
			min_temp = None
			max_temp = None
			precip = fa[i]
			min_temp = fb[i]
			max_temp = fc[i]
			insert_data = (row, col, precip, min_temp, max_temp, i, year, month, day)
			self.insert_row(insert_statement, insert_data)

    def insert_row(data):
       self.curs.execute(self._insert_statement, insert_data)
	
        

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



#Defines an interface to our database

from pysqlite2 import dbapi2 as sqlite3
import datetime

class ClimateGridInterface:
	"""
	Defines some interface methods for our ClimateGrid table
	Automatically connects to the db upon creation and creates the necessary tables
	"""

	conn = None	 #db connection
	curs = None	 #cursor for connection

	def __init__(self):
	#Docs for pysqlite: http://pysqlite.googlecode.com/svn/doc/sqlite3.html
		self.conn = sqlite3.connect("./testdb.sqlite")
		self.conn.isolation_level = "DEFERRED"
		self.curs = self.conn.cursor()
		#TODO: test for existence of our db, create only if necessary
		#Using try/except.
		try:
			self.curs.execute(self._create_statement)
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

	# TODO: implement this
	_retrieve_statement = """
		SELECT * FROM ClimateGrid WHERE """

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
		row = (lat + 90) * _nrows / 180
		col = (lng + 180) * _ncols / 360
		row = int(row) % _nrows
		col = int(col) % _ncols
		return (row, col)

	def index_to_sequence(self, row, col):
		"""
		Converts a (row, col) index to a sequence number
		"""
		return col * 720 + row

	def import_files(self, fa, fb, fc, year, month, day, doy):
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
			date = "%04d%02d%02d" % (year, month, day)
			insert_data = (row, col, precip, min_temp, max_temp, i, date)
			self.insert_row(insert_data)

	def insert_row(self, data):
	   self.curs.execute(self._insert_statement, data)
	   
	def retrieve_row(self, data):
		#Uncomment this when this is done
		#result = self.curs.execute(self._retrieve_statement, data)
		print data
		result = (10, 44, 0.0, 3.265, 8.458, 364, 2006, 12, 30)
		return result
	
	


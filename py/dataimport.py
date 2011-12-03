#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, tarfile
from pysqlite2 import dbapi2 as sqlite3
import datetime


def import_file(filename1, filename2, filename3):
	
	print "Reading files...",
	
	# Split each file into items.
	fa = open(filename1, 'r').read().split()
	fb = open(filename2, 'r').read().split()
	fc = open(filename3, 'r').read().split()
	
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
	
	
	class Helper:
		@staticmethod
		def index_to_sequence(row, col):
			"""Converts a (row, col) index to a sequence number
			"""
			return col * 720 + row
	
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
	
	#connect can take a file path for a db file, or ':memory:' to create a db in RAM
	conn = sqlite3.connect(':memory:')
	c = conn.cursor()
	c.execute(create_statement)
	
	year = int(filename1.split(".")[-2][:4])
	month = int(filename1.split(".")[-2][4:6])
	day = int(filename1.split(".")[-2][6:8])
	start = datetime.datetime(year, 1, 1)
	now = datetime.datetime(year, month, day)
	doy = (now-start).days
	
	for i in xrange(len(fa)):
		row, col = int(i/360),i%720
		precip = None
		min_temp = None
		max_temp = None
		precip = fa[i]
		min_temp = fb[i]
		max_temp = fc[i]
		insert_data = (row, col, precip, min_temp, max_temp, i, year, month, day)
		c.execute(insert_statement, insert_data)
	
	print "Success!"
	
	print(c.execute("SELECT * FROM ClimateGrid WHERE Row = 80 AND Col = 135").fetchall())

	conn.close()
if __name__=="__main__":
	if len(sys.argv)<4:
		print "Not enough arguments!"
		sys.exit(1)
	import_file(sys.argv[1], sys.argv[2], sys.argv[3])
else:
	print __name__

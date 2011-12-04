#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, tarfile
import datetime
from dbinterface import ClimateGridInterface

#Usage:
# p='../data/test'
# python dataimport.py $p/pre.20061231.asc $p/tmin.20061231.asc $p/tmax.20061231.asc

def import_file(filename1, filename2, filename3):
	print "Reading files...",
	
	# Split each file into items.
	fa = open(filename1, 'r').read().split()
	fb = open(filename2, 'r').read().split()
	fc = open(filename3, 'r').read().split()
	
	year = int(filename1.split(".")[-2][:4])
	month = int(filename1.split(".")[-2][4:6])
	day = int(filename1.split(".")[-2][6:8])
	start = datetime.datetime(year, 1, 1)
	now = datetime.datetime(year, month, day)
	doy = (now-start).days

	cgi = ClimateGridInterface()
	cgi.import_files(fa, fb, fc, year, month, day, doy)
	
	print("Imported %(year)s/%(month)s/%(day)s" % { 'year': year, 'month': month, 'day': day })
	
	#print(cgi.curs.execute("SELECT * FROM ClimateGrid WHERE Row = 80 AND Col = 135").fetchall())

if __name__=="__main__":
	if len(sys.argv)<4:
		print "Not enough arguments!"
		sys.exit(1)
	import_file(sys.argv[1], sys.argv[2], sys.argv[3])
else:
	print __name__

#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright Jon Berg , turtlemeat.com

import string,cgi,time,json
import dbinterface
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pri

class MyHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			if self.path.endswith(".html"):
				f = open(curdir + sep + self.path) #self.path has /test.html
#note that this potentially makes every file on your computer readable by the internet

				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
				return
			if "?" in self.path:   #our dynamic content
				# safe eval: restrict all namespaces to prevent url injection
				data = eval("{'"+",'".join(self.path.split("?")[-1].split("&")).replace("=","':")+"}",{"__builtins__":None},{})
				self.send_response(200)
				self.send_header('Content-type',	'text/html')
				self.end_headers()
				self.wfile.write(json.dumps(dbinterface.ClimateGridInterface().retrieve_row(data)))
				return
			
			return
				
		except IOError:
			self.wfile.write("404: FileNotFound!")
			self.send_error(404,'File Not Found: %s' % self.path)
     

	def do_POST(self):
		global rootnode
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				query=cgi.parse_multipart(self.rfile, pdict)
			self.send_response(301)
            
			self.end_headers()
			upfilecontent = query.get('upfile')
			print "filecontent", upfilecontent[0]
			self.wfile.write("<HTML>POST OK.<BR><BR>");
			self.wfile.write(upfilecontent[0]);
			
		except :
			pass

def main():
    try:
        server = HTTPServer(('', 80), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

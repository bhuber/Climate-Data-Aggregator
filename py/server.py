#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright Jon Berg , turtlemeat.com

import string,cgi,time,json
import dbinterface
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import re
#import pri

floatx = '[-+]?[0-9]*\\.?[0-9]+'

class MyHandler(BaseHTTPRequestHandler):
    grid_endpoint_regex = '^/grid/(?P<lat>%s)/(?P<lng>%s)/$' % (floatx, floatx)
    _grid_matcher = re.compile(grid_endpoint_regex)
    dbi = dbinterface.ClimateGridInterface()

    def __init__(self, request, clientaddress, server):
        BaseHTTPRequestHandler.__init__(self, request, clientaddress, server)

    def do_GET(self):
        print(self.path)
        try:
            matches = self._grid_matcher.match(self.path)
            if self.path.endswith(".html"):
                #I really don't want people reading my machine....
                raise(Exception("Sorry, can't read files on my compy"))

                f = open(curdir + sep + self.path) #self.path has /test.html
                                #note that this potentially makes every file on your computer readable by the internet

                self.send_response(200)
                self.send_header('Content-type',        'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            elif "?" in self.path:   #our dynamic content
                # safe eval: restrict all namespaces to prevent url injection
                data = eval("{'"+",'".join(self.path.split("?")[-1].split("&")).replace("=","':")+"}",{"__builtins__":None},{})
                self.send_response(200)
                self.send_header('Content-type',        'text/html')
                self.end_headers()
                self.wfile.write(json.dumps(dbinterface.ClimateGridInterface().get_row_by_xy(data)))
                return

            elif matches is not None:
                lat = matches.group("lat")
                lng = matches.group("lng")
                print(lat, lng)
                xy = { 'x': float(lng), 'y': float(lat) }
                rows = self.dbi.get_row_by_xy(xy)
                result = dict()
                data = []
                result['header'] = ["Precip", "Min_T", "Max_T", "Date"]
                for r in rows:
                    myrow = list(r)
                    #Convert u'20061231' to '20061231'
                    #TODO: there must be a better way to do this...
                    myrow[3] = str(eval(myrow[3]))
                    data.append(myrow)

                result['data'] = data
                #print(rows)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(result);
                return
                    
            else:
                self.wfile.write("404: FileNotFound!")
                self.send_error(404,'File Not Found: %s' % self.path)

        except IOError:
            self.wfile.write("404: FileNotFound!")
            self.send_error(404,'File Not Found: %s' % self.path)
        except Exception:
            self.wfile.write("500: Internal Server Error!")
            self.send_error(500,'Internal Server Error: %s' % self.path)
            


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
        server = HTTPServer(('', 8001), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>{0}</h1><p>{1}</p></body></html>")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        # self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        self.log_message( "Command: %s Path: %s Headers: %r"
                          % ( self.command, self.path, self.headers.items() ) )
        if self.headers.has_key('content-length'):
            length= int(self.headers['content-length'])
            self.log_message('Length of content: %s') % int(self.headers['content-length'])
            self.ingest_vlpro_alarm(self.rfile.read(length))
        else:
            self.ingest_vlpro_alarm(None)
    def ingest_vlpro_alarm(self, formInput=None):
        #Take the alert from VLPro
        response= "<html><head></head><body>"
        response+= "<p>HTTP Request</p>"
        response+= "<p>self.command= <tt>%s</tt></p>" % ( self.command )
        response+= "<p>self.path= <tt>%s</tt></p>" % ( self.path )
        response+= "</body></html>"
        self.wfile.write(response)

def run(server_class=HTTPServer, handler_class=S, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

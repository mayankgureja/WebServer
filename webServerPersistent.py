"""
webServer.py
Mayank Gureja
02/06/2013
ECEC 433
"""

import BaseHTTPServer
import time
import os
import cgi
import uasparser
import random
import urlparse


# Global Variables
serverHost = 'localhost'
# serverHost = '192.168.0.3'
serverPort = 22222
images = ["twitter.jpg", "facebook.jpg", "youtube.jpg"]


class WebServer(BaseHTTPServer.BaseHTTPRequestHandler):

    def setup(self):
        """
        Constructor for WebServer class
        """
        BaseHTTPServer.BaseHTTPRequestHandler.setup(self)
        self.rfile._sock.settimeout(120)  # 120 second timeout for connection
        self.protocol_version = 'HTTP/1.1'  # Enable persistent connections

    def do_GET(self):
        """
        Handler for the GET requests
        """

        # print "\n\nUser-agent: %s\n" % str(self.headers['user-agent'])
        userAgent = self.userAgentParser()

        # Parse URL
        url = urlparse.urlparse(self.path)
        # print "%s" % str(url)
        url_qs = urlparse.parse_qs(self.path)
        # print "%s" % str(url_qs)

        if self.path.endswith(".jpg"):  # Send back image
            f = open(os.getcwd() + "\\pics\\" + random.choice(images), "rb")  # Open image
            # print os.path.abspath(f.name)

            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Content-Length', os.fstat(f.fileno()).st_size)  # Find byte-size of image
            self.send_header('Connection', 'Close')
            self.end_headers()

            self.wfile.write(f.read())
            f.close()

        elif self.path.endswith("post"):  # POST command test
            f = open(os.getcwd() + "\\pics\\" + random.choice(images),
                     "rb").read().encode('base64').replace('\n', '')  # Open for use as inline object

            img_tag = '<img src="data:image/jpeg;base64,{0}">'.format(f)  # HTML string for <img> tag

            response = "<html>\r\n"
            response += "<p><h1>POST data to server</h1></p>\r\n"
            response += "<p>Hello! How may I serve you today?</p>\r\n"
            response += "<p>Current Time: " + time.strftime("%Y-%m-%d %H:%M:%S") + "</p>\r\n"
            response += "<p>You are using: %s on %s</p>" % (userAgent[0], userAgent[1])
            response += "<p><a href=\"%s\">%s</a></p>\r\n" % (self.path.strip("post"), img_tag)
            response += "<p><form name=\"input\" action=\"#\" method=\"post\">\r\n"
            response += "Data: <input type=\"text\" name=\"data\"\r\n>"
            response += "<input type=\"submit\" value=\"Submit\"></p>\r\n"
            response += "</html>\r\n"

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(response))
            self.end_headers()

            self.wfile.write(response)

        elif self.path == "/":  # Homepage
            f = open(os.getcwd() + "\\pics\\" + random.choice(images),
                     "rb").read().encode('base64').replace('\n', '')  # Open for use as inline object

            img_tag = '<img src="data:image/jpeg;base64,{0}">'.format(f)  # HTML string for <img> tag

            response = "<html>\r\n"
            response += "<p><h1>Homepage</h1></p>\r\n"
            response += "<p>Hello! How may I serve you today?</p>\r\n"
            response += "<p>Current Time: " + time.strftime("%Y-%m-%d %H:%M:%S") + "</p>\r\n"
            response += "<p>You are using: %s on %s</p>\r\n" % (userAgent[0], userAgent[1])
            response += "<p><a href=\"%s\">%s</a></p>\r\n" % (self.path, img_tag)
            response += "<p><a href=\"%simage.jpg\" />Test Image</a>\r\n" % self.path
            response += "&nbsp;&nbsp;&nbsp;&nbsp;<a href=\"%spost\" />Test POST</a>\r\n" % self.path
            response += "&nbsp;&nbsp;&nbsp;&nbsp;<a href=\"%supload\" />Test File Upload</a></p>\r\n" % self.path
            response += "</html>\r\n"

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(response))
            self.end_headers()

            self.wfile.write(response)

        elif self.path.endswith("upload"):  # upload command
            f = open(os.getcwd() + "\\pics\\" + random.choice(images),
                     "rb").read().encode('base64').replace('\n', '')  # Open for use as inline object

            img_tag = '<img src="data:image/jpeg;base64,{0}">'.format(f)  # HTML string for <img> tag

            response = "<html>\r\n"
            response += "<p><h1>Upload file AND have it displayed back to you</h1></p>\r\n"
            response += "<p>Hello! How may I serve you today?</p>\r\n"
            response += "<p>Current Time: " + time.strftime("%Y-%m-%d %H:%M:%S") + "</p>\r\n"
            response += "<p>You are using: %s on %s</p>" % (userAgent[0], userAgent[1])
            response += "<p><a href=\"%s\">%s</a></p>\r\n" % (self.path.strip("upload"), img_tag)
            response += "<p><form name=\"upload\" enctype=\"multipart/form-data\" action=\"#\" method=\"post\">\r\n"
            response += "Select file: <input type=\"file\" name=\"file\"\r\n>"
            response += "<input type=\"submit\" value=\"Upload\"></p>\r\n"
            response += "</html>\r\n"

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(response))
            self.end_headers()

            self.wfile.write(response)

        else:  # Page Not Found
            self.send_error(404)

        return

    def do_HEAD(self):
        """
        Handler for the HEAD requests
        """
        self.send_error(501)
        return

    def do_POST(self):
        """
        Handler for the POST requests
        """

        userAgent = self.userAgentParser()

        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })

        response = "Client: %s\n" % str(self.client_address)
        response += "User-Agent: %s on %s\n" % (userAgent[0], userAgent[1])
        response += "Path: %s\n" % self.path
        response += "Form data:"

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:  # The field contains an uploaded file
                file_data = field_item.file.read()  # Read file contents
                open('files/' + os.path.basename(field_item.filename),
                     'wb').write(file_data)  # Save file in /files on server
                file_len = len(file_data)  # Find byte length of file

                response += "\nFile %s uploaded\n" % (field_item.filename)
                response += "\tUploaded %s (%d bytes)\n" % (field, file_len)
                response += "\n\n\nFile contains the following:\n\n\n%s" % file_data

                del file_data
            else:
                # Regular form value
                response += "\nRaw data uploaded\n"
                response += "\t%s = %s\n" % (field, form[field].value)

        self.send_response(200)
        self.send_header('Content-Length', len(response))
        self.end_headers()

        self.wfile.write(response)
        return

    def do_UPDATE(self):
        """
        Handler for the UPDATE requests
        """
        self.send_error(501)
        return

    # Parses User-Agent information
    def userAgentParser(self):
        """
        Parses User-Agent information
        """
        uas = uasparser.UASparser()
        result = uas.parse(self.headers['user-agent'])
        print "\n\nUser Agent: \n%s: %s - OS: %s\n" % (result['typ'], result['ua_name'], result['os_name'])
        return result['ua_name'], result['os_name']


def main():
    """
    main
    """

    try:
        # Create a web server and define the handler to manage the
        # incoming request
        server = BaseHTTPServer.HTTPServer((serverHost, serverPort), WebServer)
        print "INFO: I am listening at %s" % (str(server.socket.getsockname()))
        print "* Web Server is ready to accept connections! *\n"

        # Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print "\nINFO: KeyboardInterrupt"

        print "* Closing all sockets... *\n"
        server.server_close()

        for i in range(3, 0, -1):
            time.sleep(1)
            print "* Exiting in... %s second(s) *" % i

        print "\n* Goodbye! *\n"
        time.sleep(1)
        exit(0)


# Entry point
if __name__ == "__main__":
    main()

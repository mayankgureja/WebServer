WebServer-Python
================

A Web Server with GET, POST and File Uploading, written in Python


How To Run
----------

Just launch webServer*.py. There are no parameters.


Compatibility
-------------

Tested to work on Google Chrome, Firefox, Internet Explorer, Google Chrome for Android and Android Web Browser


Description
-----------

webServer*.py is a Web Server written in Python. It uses the BaseHTTPServer library to create sockets and run an always-on web service. The advantage of having used BaseHTTPServer is less coding (fewer lines), no need to implement select.select() (it's built-in) and greater flexibility and ease in coding more advanced functions.

webServerPersistent.py has a connection timeout of 120 seconds and uses HTTP 1.1 that allows for persistent connections. webServerNonPersistent.py has no custom timeout limit and no persistence, so connectionc close immediately (faster). Content-Length is sent with every request so the client knows how much information to expect and close the connection accordingly.

It has been tested to work Google Chrome, Firefox, Internet Explorer, Google Chrome for Android and Android Web Browser.

When a bad GET request comes in, the server will send back a 404 Not Found error.

The server does not crash for any reason. It simply displays the error message and continues.


Bells & Whistles
------------------

1. POST: The web server is capable of handling POST requests. Simply go to localhost:22222/post and the new page with a form loads. Anything submitted from this form is POSTed to the server.
2. UPLOAD: The web server is capable of uploading files onto itself. Go to localhost:22222/upload and a new page with a form loads. Uploading a text file here will take the user to a new page, where the text file's size and contents are displayed. The file is saved in the /files folder
3. URL PARSING: The web server is capable of parsing URLs in the GET request, although this functionality has not been used.
4. RANDOM IMAGES: The web pages the server loads all contain inline images. These are stored in the /pics folder and are chosen at random.
5. USER-AGENT PARSING: An external library called [UASParser](http://user-agent-string.info/download/UASparser-for-Python) has been used to parse the user-agent information being received from the client. This information is displayed on the console as well as the web pages. Although this information is never used to do something specific with a certain type of web browser, it is definitely possible to do.
6. IMAGE/JPEG: Going to localhost:22222/image.jpg or /.jpg or any link ending with a ".jpg" will do a type/jpeg GET on the server and again a random image is fetched from the /pics folder.
7. ERROR 501: If a HEAD or UPDATE request is received by the server, it will return a 501 Not Implemented error.
8. KEYBOARD INTERRUPT: As an added UI touch, a keyboard interrupt on the server will display a 5 second countdown before the server quits. This really has no use, it's just a cosmetic feature.


Problems
--------

One issue that was found with the server was with the use of persistent connections. When persistent connections are turned off, everything works just fine as would be expected from a web server.

However, when persistent connections are turned on (by setting protocol_version to 'HTTP/1.1', a problem arises. When a browser makes a connection to the server, it is persistent. Therefore, even after all the information has been sent to the client, the server and client keep the connection open. This length is decided upon by the type of browser. Even though Content-Length is specified by the server, the connection is meant to persist. Different browsers handle persistence differently. For example, Firefox keeps the connection open for 115 seconds before termiating. Chrome keeps it open for a bit less, etc. The problem with this is that when Firefox has opened a connection, it can keep browsing through anything on the web server. But if Chrome now tries to access this server, it will be blocked and will keep waiting to load. This is because Firefox has the connection open and will not close it because of persistence. Until Firefox reaches its persistent connection timeout, Chrome will not be able to get in. A solution to this problem was not found, if it is even possible.

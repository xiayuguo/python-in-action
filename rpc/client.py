from xmlrpclib import ServerProxy

svr = ServerProxy("http://localhost:8080")

svr.hello()
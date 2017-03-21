from SimpleXMLRPCServer import SimpleXMLRPCServer

def hello():
	print("hello, world")


svr = SimpleXMLRPCServer(("", 8080), allow_none=True)
svr.register_function(hello)
svr.serve_forever()

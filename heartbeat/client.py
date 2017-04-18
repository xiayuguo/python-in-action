#!/usr/bin/python
#encoding:utf-8

'''
client
'''

import socket, sys, os
import time, json

host = socket.gethostname()  # 这里获取的是本地，具体视情况而定
port = 7878
BUF_SIZE = 4096

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, e:
    print "Error creating socket: %s" % e
    sys.exit()

try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    print "Hostname couldn't be resolved. Exciting"

    sys.exit()

try:
    client.connect((remote_ip, port))
    client.setblocking(0)   # set the socket is not blocking
    print "Socket connected to %s on ip %s" % (host, remote_ip)
except socket.gaierror, e:  #address related error
    print "connected to server error%s" % e
    sys.exit()


# beat_count = 0

#send heart_beat
while True:
    # beat_count += 1 #heart_beat time

    host_name = socket.gethostname()
    data_to_server = {'ip': socket.gethostbyname(host_name), 'status': 'alive', 'pid': os.getpid()}
    data_dumped = json.dumps(data_to_server)
    try:
        client.sendall(data_dumped)
    except socket.error:
        print "Send failed!!"
        sys.exit()

    print 'I - ', os.getpid(), '- am alive.'
    time.sleep(3)
client.close()

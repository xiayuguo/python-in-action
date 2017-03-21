import sys
from config import redisdb


if __name__ == '__main__':
    channel = sys.argv[1]
    pubsub = redisdb.pubsub()
    pubsub.subscribe(channel)
    
    print 'Listening to {channel}'.format(**locals())

    while True:
        for item in pubsub.listen():
            print item['data']

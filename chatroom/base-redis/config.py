import redis

config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

redisdb = redis.StrictRedis(**config)


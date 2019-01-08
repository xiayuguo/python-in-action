"""

    Version 4.0 introduced new lower case settings and setting organization.

    The major difference between previous versions, apart from the lower case names,
    are the renaming of some prefixes, like celerybeat_ to beat_, celeryd_ to worker_,
    and most of the top level celery_ settings have been moved into a new task_ prefix.

    if you want to get more details,
        please visit http://docs.celeryproject.org/en/latest/userguide/configuration.html#new-lowercase-settings.

"""


# 使用 Redis 作为代理人
broker_url = 'redis://127.0.0.1:6379/0'

# 使用 Redis 来存储任务的状态和结果
result_backend = "redis://127.0.0.1:6379/1"

# 设置时区
timezone = 'Asia/Shanghai'

# 设置序列化的方式, 默认为json
accept_content = ['msgpack', 'json']

from flask_caching import Cache
import os

cache = Cache(
    config={
        'CACHE_TYPE': 'RedisCache',
        'CACHE_REDIS_URL': os.getenv('REDIS_URL', 'redis://localhost:6379'),
        'CACHE_DEFAULT_TIMEOUT': 500
    })

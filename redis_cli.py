from rediscluster import RedisCluster

redis_client = RedisCluster.from_url(
    url='redis://:password@127.0.0.1:6379/0',
    password='password',
    decode_responses=True
)

import redis


def get_redis_master(host,port,password=None,db=15):
    return redis.Redis(host=host, port=port, password=password, db=db, decode_responses=True)

